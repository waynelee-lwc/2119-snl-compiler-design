/*
    词法分析过程可能用到的对象，方便直接转json
*/

//Token对象，接受 类型，名称，行号
class Token{

    constructor(type,name,line,col){
        this.type = type
        this.name = name
        this.line = line
        this.col = col
    }

}
//错误对象， 接受 行号，列号，错误详情
class Error{

    constructor(err,line = 0,col = 0){
        this.line = line
        this.col = col
        this.err = err
    }

    setLine(line){
        this.line = line
        return this
    }

    setCol(col){
        this.col = col
        return this
    }
}
//日志对象
class Log{

    constructor(stateName,line,col,log,error){
        this.stateName = stateName
        this.line = line
        this.col = col
        this.log = log
        this.error = error
    }
}
//FDA状态节点
class StateVertex{

    constructor(name,parse){
        this.name = name
        this.parse = parse
    }

    //状态初始化
    init(line,col,tokenStr = ''){
        this.tokenStr = tokenStr//当前字符串
        this.line = line        //起始字符所在行
        this.beginCol = col     //起始字符所在列
        this.endCol = col - 1   //最终字符所在列
        return this
    }

    //标准解析返回值
    newResponse(){
        return new function(){
            return {
                error       : null,         //错误
                isTokenEnd  : false,        //token解析结束
                isParseEnd  : false,        //程序解析结束
                nextState   : null,         //解析后状态
                log         : null,         //日志
                goback      : 0,            //回退步数
                tokenStr    : this.tokenStr,//当前节点token内容
                token       : null          //生成token，节点结束时用
            }
        }()
        
    }

    //添加一个新字符
    addChar(ch){
        this.tokenStr += ch
        this.endCol ++
    }

    //正常解析日志
    getParseLog(ch){
        return new Log(this.name,this.line,this.endCol,`parse char : '${ch}'`,null)
    }

    //错误日志
    getErrorLog(error){
        return new Log(this.name,this.line,this.endCol,`parse failed : ${error.err}`,error)
    }

    //非解析且转移日志
    getTransitionWithoutParsingLog(nextState){
        return new Log(this.name,this.line,this.endCol,`transfer state to '${nextState.name}' without parsing`)
    }

    //解析且转移日志
    getTransitionWithParsingLog(nextState,ch){
        return new Log(this.name,this.line,this.endCol,`transfer state to '${nextState.name}' with parsing '${ch}'`)
    }

    //状态转移日志
    getTransitionLog(nextState){
        return new Log(this.name,this.line,this.endCol,`transfer state to '${nextState.name}'`)
    }

    //非法字符错误
    getIllegalCharacterError(ch){
        return new Error(`illegal character '${ch}'`,this.line,this.beginCol)
    }
    //解析冒号出错
    getErrorNextColon(ch){
        return new Error(`error next color ${ch}`,this.line,this.beginCol)
    }
    //解析字符出错
    getErrorInChar(ch){
        return new Error(`error when parsing a char ${ch}`,this.line,this.beginCol)
    }
    //未定义错误
    getUndefinedError(ch){
        return new Error(`caught an undefined error ! ${ch}`,this.line,this.beginCol)
    }
    //解析数字出错
    getErrorInNum(ch){
        return new Error(`error when parsing a number ${this.tokenStr} but ${ch}`,this.line,this.beginCol)
    }
    //程序不完整
    getNeedDotError(){
        return new Error(`need a dot at the end of program!`,this.line,this.beginCol)
    }
}

module.exports = {
    Log         : Log,
    StateVertex : StateVertex,
    Token       : Token,
    Error       : Error
}