var models = require('./models')
var checking = require('../checking')
var errors = require('./errors')
var tokens = require('./tokens')
const { Blank, Seperator } = require('../dict')
/**
 * DFA自动机状态节点
 * 把状态节点定义在这个文件中，创建时传入指定状态名称，parse方法和
 * 
 * parse方法接受一个字符，在当前状态中处理该字符，返回一个约定的response
 *      约定的response包括以下内容
 *          error           obj     错误，默认为null，当处理出错时表示错误
 *          isTokenEnd      bool    当前token解析是否结束
 *          isParseEnd      bool    当前程序解析是否结束
 *          nextState       obj     自动机的下一个状态
 *          log             obj     处理日志
 *          goback          number  回退步数
 *          tokenStr        string  当前节点的token内容，token内容不需要向后传递时为空
 *          token           obj     节点生成token，当节点结束且有token生成时返回，否则为空
 * 
 * 处理中的错误（商议）：
 *  总体上，过程中产生的错误返回并收集，不影响整个程序执行
 *  如果是非法字符错误，产生错误，不回退，保留当前状态
 *  如果是合法字符但是处在非合法位置，产生错误，回退当前字符（回退量待验证），转起始状态
 */

const START         = 'START'
const INID          = 'INID'
const INNUM         = 'INNUM'
const INSEPERATOR   = 'INSEPERATOR'
const INCOMMENT     = 'INCOMMENT'
const INCOLON       = 'INCOLON'
const INASSIGN      = 'INASSIGN'
const INCHAR        = 'INCHAR'
const DONECHAR      = 'DONECHAR'
const INDOT         = 'INDOT'
const INRANGE       = 'INRANGE'
const DONE          = 'DONE'
module.exports = {
    ...models.exports,
    START       : START,
    INID        : INID,
    INNUM       : INNUM,
    INSEPERATOR : INSEPERATOR,
    INCOMMENT   : INCOMMENT,
    INCOLON     : INCOLON,
    INASSIGN    : INASSIGN,
    INCHAR      : INCHAR,
    DONECHAR    : DONECHAR,
    INDOT       : INDOT,
    INRANGE     : INRANGE,
    DONE        : DONE

}

const Start         = new models.StateVertex(START      ,function(ch){
    res = this.newResponse()

    //非法字符
    if(!checking.IsLegal(ch)){
        res.isTokenEnd  = true
        res.nextState   = this
        res.error       = this.getIllegalCharacterError(ch)
        res.log         = this.getErrorLog(res.error)
        return res
    }
    //空白字符
    if(checking.IsBlankSpace(ch)){
        res.nextState   = this
        res.log         = this.getParseLog(ch)
        return res
    }
    //字母
    if(checking.IsLetter(ch)){
        res.isTokenEnd  = true
        res.nextState   = InID
        res.log         = this.getTransitionLog(InID)
        res.goback      = 1
        return res
    }
    ///数字
    if(checking.IsNumber(ch)){
        res.isTokenEnd  = true
        res.nextState   = InNum
        res.log         = this.getTransitionLog(InNum)
        res.goback      = 1
        return res
    }
    //分隔符
    if(checking.IsSeperator(ch)){
        res.isTokenEnd  = true
        res.nextState   = InSeperator
        res.log         = this.getTransitionLog(InSeperator)
        res.goback      = 1
        return res
    }
    //注释头符
    if(checking.IsCommentHeader(ch)){
        res.isTokenEnd  = true
        res.nextState   = InComment
        res.log         = this.getTransitionLog(InComment)
        res.goback      = 0
        return res
    }
    //冒号
    if(checking.IsColon(ch)){
        res.isTokenEnd  = true
        res.nextState   = InColon
        res.log         = this.getTransitionLog(InColon)
        res.goback      = 0
        res.tokenStr    = ch
        return res
    }
    //点符
    if(checking.IsDot(ch)){
        res.isTokenEnd  = true
        res.nextState   = InDot
        res.log         = this.getTransitionLog(InDot)
        res.goback      = 0
        return res
    }
    //单引号
    if(checking.isApostrophe(ch)){
        res.isTokenEnd  = true
        res.nextState   = InChar
        res.log         = this.getTransitionLog(InChar)
        res.goback      = 0
        return res
    }
    //EOF
    if(checking.isEOF(ch)){
        res.isTokenEnd  = true
        res.IsParseEnd  = true
        return res
    }
    //其他字符
    res.log   = this.getErrorLog(this.getUndefinedError(ch))
    res.error = this.getUndefinedError(ch)
    return res
})
const InID          = new models.StateVertex(INID       ,function(ch){
    res = this.newResponse()
    //非法字符
    if(!checking.IsLegal(ch)){
        res.isTokenEnd  = true
        res.nextState   = Start
        res.error       = this.getIllegalCharacterError(ch)
        res.log         = this.getErrorLog(res.error)
        return res
    }
    //字母数字
    if(checking.IsLetter(ch) || checking.IsNumber(ch)){
        this.addChar(ch)
        res.log     = this.getParseLog(ch)
        return res
    }
    //其他合法字符
    res.isTokenEnd  = true
    res.nextState   = Start
    res.log         = this.getTransitionLog(Start)
    res.goback      = 1
    if(checking.IsReserved(this.tokenStr)){
        res.token = tokens.GetToken(tokens.RESERVED,this.tokenStr,this.line,this.beginCol)
    }else{
        res.token = tokens.GetToken(tokens.ID,this.tokenStr,this.line,this.beginCol)
    }
    return res
})
const InNum         = new models.StateVertex(INNUM      ,function(ch){
    res = this.newResponse()
    //非法字符
    if(!checking.IsLegal(ch)){
        res.isTokenEnd  = true
        res.nextState   = Start
        res.error       = this.getIllegalCharacterError(ch)
        res.log         = this.getErrorLog(res.error)
        return res
    }
    //数字
    if(checking.IsNumber(ch)){
        this.addChar(ch)
        res.log     = this.getParseLog(ch)
        return res
    }
    //字母，报错
    if(checking.IsLetter(ch)){
        res.isTokenEnd  = true
        res.nextState   = Start
        res.error       = this.getErrorInNum(ch)
        res.log         = this.getErrorLog(res.error)
        res.goback      = 1
        return res
    }
    //其他字符，生成token
    res.isTokenEnd  = true
    res.nextState   = Start
    res.log         = this.getTransitionLog(Start)
    res.token       = tokens.GetToken(tokens.NUMBER,this.tokenStr,this.line,this.beginCol)
    res.goback      = 1
    return res
})
const InSeperator   = new models.StateVertex(INSEPERATOR,function(ch){
    res = this.newResponse()
    //非法字符
    if(!checking.IsLegal(ch)){
        res.isTokenEnd  = true
        res.nextState   = Start
        res.error       = this.getIllegalCharacterError(ch)
        res.log         = this.getErrorLog(res.error)
        return res
    }
    //分界符
    if(checking.IsSeperator(ch)){
        this.addChar(ch)
        res.token       = tokens.GetToken(tokens.SEPERATOR,this.tokenStr,this.line,this.beginCol)
        res.isTokenEnd  = true
        res.nextState   = Start
        res.log         = this.getParseLog(ch)
        return res
    }
    //其他字符
    res.isTokenEnd  = true
    res.nextState   = Start
    res.token       = tokens.GetToken(tokens.SEPERATOR,this.tokenStr,this.lien,this.beginCol)
    res.log         = this.getTransitionLog(Start)
    res.goback      = 1
    return res
})
const InComment     = new models.StateVertex(INCOMMENT  ,function(ch){
    res = this.newResponse()
    //非法字符
    // if(!checking.IsLegal(ch)){
    //     res.isTokenEnd  = true
    //     res.nextState   = Start
    //     res.error       = this.getIllegalCharacterError(ch)
    //     res.log         = this.getErrorLog(res.error)
    //     return res
    // }
    //注释尾符
    if(checking.IsCommentEnder(ch)){
        res.isTokenEnd  = true
        res.nextState   = Start
        res.log         = this.getTransitionLog
        res.comment     = {comment:this.tokenStr ,line : this.line}
        return res
    }
    //其他符号
    this.addChar(ch)
    res.log     = this.getParseLog(ch)
    return res
})
const InColon       = new models.StateVertex(INCOLON    ,function(ch){
    res = this.newResponse()
    //非法字符
    if(!checking.IsLegal(ch)){
        res.isTokenEnd  = true
        res.nextState   = Start
        res.error       = this.getIllegalCharacterError(ch)
        res.log         = this.getErrorLog(res.error)
        return res
    }
    //等号
    if(checking.isEqualSign(ch)){
        res.isTokenEnd  = true
        res.nextState   = InAssign
        res.log         = this.getTransitionLog(InAssign)
        return res
    }
    //其他符号
    res.error       = this.getErrorNextColon(ch)
    res.log         = this.getErrorLog(res.error)
    res.isTokenEnd  = true
    res.nextState   = Start
    return res
})
const InAssign      = new models.StateVertex(INASSIGN   ,function(ch){
    res = this.newResponse()
    //非法字符
    if(!checking.IsLegal(ch)){
        res.isTokenEnd  = true
        res.nextState   = Start
        res.error       = this.getIllegalCharacterError(ch)
        res.log         = this.getErrorLog(res.error)
        return res
    }
    //其他符号
    res.isTokenEnd  = true
    res.nextState   = Start
    res.log         = this.getTransitionLog(Start)
    res.token       = tokens.GetToken(tokens.ASSIGN,':=',this.line,this.beginCol)
    res.goback      = 1
    return res
})
const InChar        = new models.StateVertex(INCHAR     ,function(ch){
    res = this.newResponse()
    //非法字符
    if(!checking.IsLegal(ch)){
        res.isTokenEnd  = true
        res.nextState   = Start
        res.error       = this.getIllegalCharacterError(ch)
        res.log         = this.getErrorLog(res.error)
        return res
    }
    //字母或数字
    if(checking.IsLetter(ch) || checking.IsNumber(ch)){
        res.isTokenEnd  = true
        res.tokenStr    = ch
        res.nextState   = DoneChar
        res.log         = this.getParseLog(ch)
        return res
    }
    //其他符号
    res.error   = this.getErrorInChar(ch)
    res.log     = tihs.getErrorLog(res.error)
    return res
})
const DoneChar      = new models.StateVertex(DONECHAR   ,function(ch){
    res = this.newResponse()
    //非法字符
    if(!checking.IsLegal(ch)){
        res.isTokenEnd  = true
        res.nextState   = Start
        res.error       = this.getIllegalCharacterError(ch)
        res.log         = this.getErrorLog(res.error)
        return res
    }
    //单引号
    if(checking.isApostrophe(ch)){
        res.isTokenEnd  = true
        res.nextState   = Start
        res.log         = this.getTransitionLog(Start)
        res.token       = tokens.GetToken(tokens.CHARC,this.tokenStr,this.line,this.beginCol)
        return res
    }
    //其他符号
    res.error   = this.getErrorInChar(ch)
    res.log     = this.getErrorLog(res.error)
    return res
})
const InDot         = new models.StateVertex(INDOT      ,function(ch){
    res = this.newResponse()
    //非法字符
    if(!checking.IsLegal(ch)){
        res.isTokenEnd  = true
        res.nextState   = Start
        res.error       = this.getIllegalCharacterError(ch)
        res.log         = this.getErrorLog(res.error)
        return res
    }
    //点符
    if(checking.IsDot(ch)){
        res.nextState   = InRange
        res.isTokenEnd  = true
        res.log         = this.getTransitionLog(InRange)
        res.goback      = 1
        return res
    }
    //空白符，程序结束，其他符号，生成点号继续解析
    res.isTokenEnd  = true
    res.token       = tokens.GetToken(tokens.SEPERATOR,'.',this.line,this.beginCol)
    if(checking.IsBlankSpace(ch) || checking.isEOF(ch)){
        res.IsParseEnd = true
        res.nextState = Done
    }else{
        res.IsParseEnd = false
        res.nextState = Start
        res.goback = 1
    }
    return res
})
const InRange       = new models.StateVertex(INRANGE    ,function(ch){
    res = this.newResponse()
    //非法字符
    if(!checking.IsLegal(ch)){
        res.isTokenEnd  = true
        res.nextState   = Start
        res.error       = this.getIllegalCharacterError(ch)
        res.log         = this.getErrorLog(res.error)
        return res
    }
    //其他符号
    res.nextState   = Start
    res.isTokenEnd  = true
    res.log         = this.getTransitionLog(Start)
    res.token       = tokens.GetToken(tokens.UNDERANGE,'..',this.line,this.beginCol)
    return res
})
const Done          = new models.StateVertex(DONE       ,function(ch){
    res = this.newResponse()
    //非法字符
    if(!checking.IsLegal(ch)){
        res.isTokenEnd  = true
        res.nextState   = Start
        res.error       = this.getIllegalCharacterError(ch)
        res.log         = this.getErrorLog(res.error)
        return res
    }
    //任意字符
    res.isTokenEnd  = true
    res.IsParseEnd  = true
    res.nextState   = Done
    return res
}) 

module.exports = {
    ...module.exports,
    Start       : Start,
    InID        : InID,
    InNum       : InNum,
    InSeperator : InSeperator,
    InComment   : InComment,
    InColon     : InColon,
    InAssign    : InAssign,
    InChar      : InChar,
    DoneChar    : DoneChar,
    InDot       : InDot,
    InRange     : InRange,
    Done        : Done
}

/**
 * 一段测试程序。
 * 解析文本，大小写字母为合法字符，其他非法报错，
 * 空格或者连续的空格会被解析成为分隔符，'.'表示结束
 * 
 * 例如：
 *   'hello world.'
 *  解析成为：
 *   'hello' ' '  'world' '.'
 * 
 * 
 * 节点类型：
 *  start   :   程序开始状态，不产生任何token，接受空白字符转blank，回退1步；接受字母转word,回退1步
 *  blank   :   空白字符解析，接受空白字符进行拼接；接受字母生成token转word,回退1步；接受'.'转end，回退1步
 *  word    :   单词解析，接受大小写字母进行拼接；接受空白字符生成token转blank，回退1步；接受'.'转end，回退1步
 *  end     :   结束状态，接受'.'；其他报错
 */

const TEST_DEMO_START = '[test]start'
const TEST_DEMO_BLANK = '[test]blank'
const TEST_DEMO_WORD  = '[test]word'
const TEST_DEMO_END   = '[test]end'

const TestDemoStart = new models.StateVertex(TEST_DEMO_START,function(ch){
    //获取新的返回值对象
    res = this.newResponse()

    //字母
    if(checking.IsLetter(ch)){
        res.nextState = TestDemoWord
        res.goback = 1
        res.isTokenEnd = true
        res.log = this.getTransitionLog(TestDemoWord)
        return res
    }

    //空格
    if(checking.IsBlankSpace(ch)){
        res.nextState = TestDemoBlank
        res.goback = 1
        res.isTokenEnd = true
        res.log = this.getTransitionLog(TestDemoBlank)
        return res
    }

    //结束符
    if(checking.IsProgramEnder(ch)){
        res.isTokenEnd = true
        res.goback = 1
        res.nextState = TestDemoEnd
        res.log = this.getTransitionLog(TestDemoEnd)
        return res
    }

    //其他字符
    res.error = this.getIllegalCharacterError(ch).setLine(this.line).setCol(this.endCol)
    res.log = this.getErrorLog(res.error)
    res.goback = 0
    res.nextState = this
    res.tokenStr = this.tokenStr

    return res
})

const TestDemoBlank = new models.StateVertex(TEST_DEMO_BLANK,function(ch){
    res = this.newResponse()

    //字母
    if(checking.IsLetter(ch)){
        res.token = tokens.GetToken(tokens.TEST_DEMO_BLANK_TOKEN_TYPE,this.tokenStr,this.line,this.beginCol)
        res.isTokenEnd = true
        res.goback = 1
        res.nextState = TestDemoWord
        res.log = this.getTransitionLog(TestDemoWord)
        return res
    }

    //空格
    if(checking.IsBlankSpace(ch)){
        this.addChar(ch)
        res.log = this.getParseLog(ch)
        return res
    }

    //程序结束符号
    if(checking.IsProgramEnder(ch)){
        res.nextState = TestDemoEnd
        res.log = this.getTransitionLog(TestDemoEnd)
        res.goback = 1
        res.isTokenEnd = true
        res.token = tokens.GetToken(tokens.TEST_DEMO_BLANK_TOKEN_TYPE,this.tokenStr,this.line,this.beginCol)
        return res
    }  

    //其他字符
    res.error = this.getIllegalCharacterError(ch).setLine(this.line).setCol(this.endCol)
    res.log = this.getErrorLog(res.error)
    res.goback = 0
    res.nextState = this
    res.tokenStr = this.tokenStr

    return res

})

//单词状态，生成token的时候判断一下保留字
const TestDemoWord = new models.StateVertex(TEST_DEMO_WORD,function(ch){
    res = this.newResponse()

    //字母
    if(checking.IsLetter(ch)){
        this.addChar(ch)
        res.log = this.getParseLog(ch)
        return res
    }

    //空格
    if(checking.IsBlankSpace(ch)){
        res.isTokenEnd = true

        if(!checking.IsReserved(this.tokenStr))
            res.token = tokens.GetToken(tokens.TEST_DEMO_WORD_TOkEN_TYPE,this.tokenStr,this.line,this.beginCol)
        else
            res.token = tokens.GetToken(tokens.TEST_DEMO_RESERVED_TOKEN_TYPE,this.tokenStr,this.line,this.beginCol)

        res.log = this.getTransitionLog(TestDemoBlank)
        res.nextState = TestDemoBlank
        res.goback = 1
        return res
    }

    //程序结束符号
    if(checking.IsProgramEnder(ch)){
        res.nextState = TestDemoEnd
        res.log = this.getTransitionLog(TestDemoEnd)
        res.goback = 1
        res.isTokenEnd = true
        
        if(!checking.IsReserved(this.tokenStr))
            res.token = tokens.GetToken(tokens.TEST_DEMO_WORD_TOkEN_TYPE,this.tokenStr,this.line,this.beginCol)
        else
            res.token = tokens.GetToken(tokens.TEST_DEMO_RESERVED_TOKEN_TYPE,this.tokenStr,this.line,this.beginCol)
        
        return res
    }

    //其他字符
    res.error = this.getIllegalCharacterError(ch).setLine(this.line).setCol(this.endCol)
    res.log = this.getErrorLog(res.error)
    res.goback = 0
    res.nextState = this
    res.tokenStr = this.tokenStr

    return res
})

const TestDemoEnd = new models.StateVertex(TEST_DEMO_END,function(ch){
    res = this.newResponse()

    //程序结束符号
    if(checking.IsProgramEnder(ch)){
        res.isTokenEnd = true
        res.IsParseEnd = true
        res.token = tokens.GetToken(tokens.TEST_DEMO_END_TOKEN_TYPE,this.tokenStr,this.line,this.beginCol)
        res.log = this.getParseLog(ch)
        res.nextState = TestDemoStart
        return res
    }

     //其他字符
     res.error = this.getIllegalCharacterError(ch).setLine(this.line).setCol(this.endCol)
     res.log = this.getErrorLog(res.error)
     res.goback = 0
     res.nextState = this
     res.tokenStr = this.tokenStr
 
     return res
})

module.exports = {
    ...module.exports,
    TEST_DEMO_BLANK     : TEST_DEMO_BLANK,
    TEST_DEMO_END       : TEST_DEMO_END,
    TEST_DEMO_START     : TEST_DEMO_START,
    TEST_DEMO_WORD      : TEST_DEMO_WORD,
    TestDemoBlank       : TestDemoBlank,
    TestDemoEnd         : TestDemoEnd,
    TestDemoStart       : TestDemoStart,
    TestDemoWord        : TestDemoWord
}