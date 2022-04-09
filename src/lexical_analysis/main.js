var ProgramReader = require('./ProgramReader')
var LexicalAnalysiser = require('./LexicalAnalysiser')
var rw = require('./rw')
var StateVertexs = require('./model/stateVertexs')
/**
 * 主方法，整个程序的入口
 * 
 * 读取文件->构建程序阅读器->构建语法分析器->语法分析->处理错误->打印token列表和日志列表
 */
function main(){

    let argv = process.argv
    let programPath = argv[2]

    if(!programPath){
        console.log('usage: node {mainfile} {programPath}')
        return
    }

    let snlFile = `${programPath}/snl`      //源代码文件
    let tkFile = `${programPath}/tk`        //token序列文件
    let errorFile = `${programPath}/lexerr` //错误信息文件
    let logFile = `${programPath}/lexlog`   //日志文件
    let commentFile = `${programPath}/cmt`  //注释文件

    let program = rw.LoadSourceCode(snlFile)
    console.log(`parsing program \n'''\n${program}\n'''`)
    reader = new ProgramReader(program)
    parser = new LexicalAnalysiser(reader,StateVertexs.Start)
    resp = parser.parse()

    // console.log('---------------------------error-----------')
    // for(let error of resp.errorList){
    //     console.log(JSON.stringify(error))
    // }
    // console.log('---------------------------token-----------')
    // for(let token of resp.tokenList){
    //     console.log(JSON.stringify(token))
    // }
    // console.log('---------------------------log-------------')
    // for(let log of resp.logList){
    //     console.log(JSON.stringify(log))
    // }

    //token list...
    rw.Save(tkFile,resp.tokenList)

    //error list...
    rw.Save(errorFile,resp.errorList)

    //log list...
    rw.Save(logFile,resp.logList)

    //comment list..
    rw.Save(commentFile,resp.commentList)
}

main()