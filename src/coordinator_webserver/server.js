let express = require('express')
let bodyParser = require('body-parser')
let fs = require('fs')
let pathTool = require('path')
let {exec, execSync} = require('child_process')
let {zip} = require('zip-a-folder')

const { dir } = require('console')

let app = express()
app.use(bodyParser.json())
app.use('/',express.static('./static'))
//跨域
app.use((req, res, next) => {
    //设置请求头
    res.set({
        'Access-Control-Allow-Credentials': true,
        'Access-Control-Max-Age': 1728000,
        'Access-Control-Allow-Origin': req.headers.origin || '*',
        'Access-Control-Allow-Headers': 'X-Requested-With,Content-Type',
        'Access-Control-Allow-Methods': 'PUT,POST,GET,DELETE,OPTIONS',
        'Content-Type': 'application/json; charset=utf-8'
    })
    req.method === 'OPTIONS' ? res.status(204).end() : next()
})

const NONE_SENSE_LEN = 10
const PORT = 3008

function formatNumber(num){
    return num < 10 ? '0'+num : ''+num
}

function currDateTime(){
    let curr = new Date()

    let year    = formatNumber(curr.getFullYear())
    let month   = formatNumber(curr.getMonth())
    let day     = formatNumber(curr.getDay())
    let hour    = formatNumber(curr.getHours())
    let minutes = formatNumber(curr.getMinutes())
    let seconds = formatNumber(curr.getSeconds())
    return `${year}-${month}-${day}_${hour}:${minutes}:${seconds}`
}

function geneRandomStr(len){
    str = ''
    for(let i = 0;i < len;i++){
        str += String.fromCharCode(Math.floor(Math.random()*26)+65)
    }
    return str
}

function geneProgramName(){
    return `${currDateTime()}_${geneRandomStr(NONE_SENSE_LEN)}`
}

function Save(dir,filename,content){
    let path = pathTool.resolve(dir,filename)

    fs.writeFileSync(path,content)
}

function Load(dir,filename){
    let path = pathTool.resolve(dir,filename)
    return fs.readFileSync(path).toString()
}

function LoadDir(path){
    let result = {}
    let files = fs.readdirSync(path)
    for(let file of files){
        str = Load(path,file)
        result[file] = str
    }
    return result
}

/* webserver */

app.post('/compile',(req,res)=>{
    // console.log(JSON.stringify(req.body))
    let src = req.body.src
    let needCache = req.body.needCache  //是否需要缓存
    let programName = geneProgramName() //生成程序文件夹名称
    let programPath = pathTool.resolve(__dirname,`../../outputs/cache/${programName}`)  //编译产物存放
    let programZip = pathTool.resolve(__dirname,`./static/zips/${programName}.zip`)     //压缩包存放地址
    let semanticAnalysis = pathTool.resolve(__dirname,`../semantic_analysis/seman.py`)  //语义分析入口地址
    let syntaxLL1Analysis = pathTool.resolve(__dirname,`../syntax_analysis/parseLL1/parse.py`)  //语法分析ll1地址

    console.log(programPath)
    fs.mkdirSync(programPath)   //创建临时产物文件夹

    Save(programPath,`snl`,src) //保存程序文件

    /**
     * TODO：
     * 判断错误不需要反复的读文件，但是赶工期就不乱改了..
     */

    /************************  词法分析  ****************************/
    let lexbuf = execSync(`node ../lexical_analysis/main.js ${programPath}`) //词法分析
    let result = LoadDir(programPath)
    if(JSON.parse(result['lexerr']).length != 0){
        //存在词法错误，返回词法错误
        let resp = {
            lex_err:result['lexerr'],
            syn_err:JSON.stringify(['','','']),
            sem_err:JSON.stringify({}),
            program_name : programName
        }
        res.send(resp)
        zip(programPath,programZip).then(()=>{
            // fs.rmdirSync(programPath,{ recursive: true, force: true })
        })
        return
    }

    /************************  语法分析  ****************************/
    let synbuf = execSync(`../syntax_analysis/recursive_descent/runnable ${programPath}`) //语法分析递归下降
    let synll1 = execSync(`python3 ${syntaxLL1Analysis} ${programPath}`)    //语法分析LL1

    // console.log(lexbuf.toString())
    // console.log(synbuf.toString())
    
    //处理语法分析结果，如果有错，不继续进行语义分析
    result = LoadDir(programPath)
    let synErr = JSON.parse(result['synerr'])
    // console.log(synErr)
    if(!synErr || synErr.length < 1 || synErr[0] != ''){
        //语法分析错误，返回token列表和语法错误
        let resp = {
            tokens :result['tk'],
            lex_err:result['lexerr'],
            syn_err:result['synerr'],
            syn_ll1_err:result['treell1err'],
            sem_err:JSON.stringify({}),
            program_name : programName
        }
        res.send(resp)
        zip(programPath,programZip).then(()=>{
            // fs.rmdirSync(programPath,{ recursive: true, force: true })
        })
        return
    }

    /************************  语义分析  ****************************/
    let sembuf = execSync(`python3 ${semanticAnalysis} ${programPath}`)
    // console.log(sembuf.toString())
    result = LoadDir(programPath)
    //无论是否出现错误，均返回全部结果
    let resp = {
        snl : result['snl'],        //源程序
        tree : result['tree'],      //递归下降语法树
        tokens : result['tk'],      //token序列
        gene : result['gene'],      //生成格式化代码
        lex_err:result['lexerr'],   //词法错误
        syn_err:result['synerr'],   //语法错误
        comments: result['cmt'],    //注释队列
        treell1: result['treell1'], //ll1生成语法树
        sem :result['sem'],         //语义分析结果
        semerr :result['semerr'],   //语义分析错误
        program_name : programName  //程序分配名称
    }
    
    /************************  结果打包  ****************************/
    zip(programPath,programZip).then(()=>{
        // fs.rmdirSync(programPath,{ recursive: true, force: true })
    })
    res.send(resp).end()
})

app.get('/demoProgramList',(req,res)=>{
    let dir = pathTool.resolve(__dirname,`../../outputs/demos`)
    files = fs.readdirSync(dir)
    res.send(files).end()
    return
})

app.get('/demoProgram',(req,res)=>{
    let dir = pathTool.resolve(__dirname,`../../outputs/demos`)
    files = fs.readdirSync(dir)
    file = req.query.file
    if(files.indexOf(file) != -1){
        res.send({demo:Load(dir,file)}).end()
    }else{
        res.send('').end()
    }
    return
})

let server = app.listen(PORT,()=>{
    console.log('The server is listening on port :',PORT)
})

