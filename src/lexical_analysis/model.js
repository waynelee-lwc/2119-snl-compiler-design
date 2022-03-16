/*
    词法分析过程可能用到的对象，方便直接转json
*/

//Token对象，接受 类型，名称，行号
exports.Token = class{

    constructor(type,name,line,col){
        this.type = type
        this.name = name
        this.line = line
        this.col = col
    }

}
//错误对象， 接受 行号，列号，错误详情
exports.Error = class{

    constructor(line,col,err){
        this.line = line
        this.col = col
        this.err = err
    }
}
//日志对象
exports.Log = class{

    constructor(line,col,log){
        this.line = line
        this.col = col
        this.log = log
    }
}
//FDA状态节点
exports.StateVertex = class{

    constructor(name,parse,getToken){
        this.name = name
        this.parse = parse
        this.getToken = getToken
    }

    init(){
        this.tokenStr = ''      //当前字符串
        this.isEnd = false      //是否结束
        this.hasError = false   //是否产生错误
        this.error = null       //错误内容
        this.line = 0           //起始字符所在行
        this.beginCol = 0       //起始字符所在列
        this.endCol = 0         //最终字符所在列
    }
}