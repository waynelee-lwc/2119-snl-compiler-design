
//语法分析器，创建的时候指定一个programReader
//执行语法分析过程，返回处理结果

const stateVertexs = require("./model/stateVertexs")
const tokens = require('./model/tokens')
const errors = require('./model/errors')

//处理结果包括 已经解析的token序列，可能出现的错误，历次解析的日志
class LexicalAnalysiser{

    constructor(reader,initState){
        this.reader = reader
        this.initState = initState
    }

    //执行解析过程，返回处理结果
    parse(){
        this.reader.reset()
        let currState = this.initState
        currState.init(1,1,'')

        let errorList   = []
        let tokenList   = []
        let logList     = []
        let commentList = []

        let needInit = true
        let tokenStr = ''
        
        // for(let i = 0;i < 300;i++){
        while(this.reader.hasNextChar()){
            //下一个字符
            let nextChar = this.reader.getNextChar()

            if(needInit){
                currState.init(nextChar.line,nextChar.col,tokenStr)
                needInit = false
                tokenStr = ''
            }
            
            //执行状态转移
            res = currState.parse(nextChar.char)
            // console.log(`goback ${res.goback} `,JSON.stringify(nextChar),JSON.stringify(res.log))
            
            //日志处理
            if(res.log){
                logList.push(res.log)
            }

            //错误处理
            if(res.error){
                errorList.push(res.error)
            }

            //注释内容处理
            if(res.comment){
                commentList.push(res.comment)
            }

            //回退处理
            this.reader.goback(res.goback)
            //生成token处理
            if(res.token){
                tokenList.push(res.token)
            }
            //节点转移处理
            if(res.nextState){
                currState = res.nextState
                needInit = true
                tokenStr = res.tokenStr
            }
            //程序解析结束
            if(res.isParseEnd){
                break;
            }
        }
        
        if(currState.name == stateVertexs.DONE){
            tokenList.push(tokens.GetToken(tokens.EOF,'EOF',this.reader.getLines() + 1,0))
        }else{
            errorList.push(currState.getNeedDotError())
        }

        //...
        return {
            errorList   : errorList,
            tokenList   : tokenList,
            logList     : logList,
            commentList : commentList
        }
    }

}
module.exports = LexicalAnalysiser