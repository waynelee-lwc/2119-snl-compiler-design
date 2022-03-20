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

    let program = rw.LoadSourceCode('mock_program.txt')
    console.log(`parsing program \n'''\n${program}\n'''`)
    reader = new ProgramReader(program)
    parser = new LexicalAnalysiser(reader,StateVertexs.Start)
    resp = parser.parse()

    console.log('---------------------------error-----------')
    for(let error of resp.errorList){
        console.log(JSON.stringify(error))
    }
    console.log('---------------------------token-----------')
    for(let token of resp.tokenList){
        console.log(JSON.stringify(token))
    }
    console.log('---------------------------log-------------')
    for(let log of resp.logList){
        console.log(JSON.stringify(log))
    }

    //error...
    rw.SaveTokens('test_output_tokens.txt',resp.tokenList)

    //token list...

    //log list...
}

main()