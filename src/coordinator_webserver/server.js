let express = require('express')
let bodyParser = require('body-parser')
let fs = require('fs')
let pathTool = require('path')
let {exec, execSync} = require('child_process')

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


/* webserver */

app.post('/compile',(req,res)=>{
    // console.log(JSON.stringify(req.body))
    let src = req.body.src
    let programName = geneProgramName()
    let programPath = pathTool.resolve(__dirname,`../../outputs/cache/${programName}`)
    console.log(programPath)
    fs.mkdirSync(programPath)

    Save(programPath,`snl`,src) //保存程序文件
    let lexbuf = execSync(`node ../lexical_analysis/main.js ${programPath}`) //词法分析
    let synbuf = execSync(`../syntax_analysis/recursive_descent/runnable ${programPath}`) //语法分析

    // console.log(lexbuf.toString())
    console.log(synbuf.toString())
    
    let result = {}
    let files = fs.readdirSync(programPath)
    for(let file of files){
        str = Load(programPath,file)
        result[file] = str
    }

    let resp = {
        snl : result['snl'],
        tree : result['tree'],
        tokens : result['tk'],
        gene : result['gene'],
        lex_err:result['lexerr'],
        syn_err:result['synerr'],
        program_name : programName
    }
    fs.rmdirSync(programPath,{ recursive: true, force: true })
    res.send(resp)
})

let server = app.listen(PORT,()=>{
    console.log('The server is listening on port :',PORT)
})

