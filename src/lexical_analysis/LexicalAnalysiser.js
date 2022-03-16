
//语法分析器，创建的时候指定一个programReader
//执行语法分析过程，返回处理结果
//处理结果包括 已经解析的token序列，可能出现的错误，历次解析的日志
export class LexicalAnalysiser{

    constructor(reader){
        this.reader = reader
        this.error = null
        this.tokenList = []
        this.logs = []
    }

    //执行解析过程，返回处理结果
    parse(){
        this.reader.reset()

        //...
        return {
            tokenList : this.tokenList,
            logs      : this.logs,
            error     : this.error
        }
    }

}