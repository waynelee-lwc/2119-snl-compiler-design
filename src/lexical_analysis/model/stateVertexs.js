var models = require('./models')
var checking = require('../checking')
var errors = require('./errors')
var tokens = require('./tokens')
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
    res = this.getNewResponse()

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
    res.error = errors.IllegalCharacterError(ch).setLine(this.line).setCol(this.endCol)
    res.log = this.getErrorLog(res.error)
    res.goback = 0
    res.nextState = this
    res.tokenStr = this.tokenStr

    return res
})

const TestDemoBlank = new models.StateVertex(TEST_DEMO_BLANK,function(ch){
    res = this.getNewResponse()

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
    res.error = errors.IllegalCharacterError(ch).setLine(this.line).setCol(this.endCol)
    res.log = this.getErrorLog(res.error)
    res.goback = 0
    res.nextState = this
    res.tokenStr = this.tokenStr

    return res

})

//单词状态，生成token的时候判断一下保留字
const TestDemoWord = new models.StateVertex(TEST_DEMO_WORD,function(ch){
    res = this.getNewResponse()

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
    res.error = errors.IllegalCharacterError(ch).setLine(this.line).setCol(this.endCol)
    res.log = this.getErrorLog(res.error)
    res.goback = 0
    res.nextState = this
    res.tokenStr = this.tokenStr

    return res
})

const TestDemoEnd = new models.StateVertex(TEST_DEMO_END,function(ch){
    res = this.getNewResponse()

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
     res.error = errors.IllegalCharacterError(ch).setLine(this.line).setCol(this.endCol)
     res.log = this.getErrorLog(res.error)
     res.goback = 0
     res.nextState = this
     res.tokenStr = this.tokenStr
 
     return res
})

module.exports = {
    TEST_DEMO_BLANK     : TEST_DEMO_BLANK,
    TEST_DEMO_END       : TEST_DEMO_END,
    TEST_DEMO_START     : TEST_DEMO_START,
    TEST_DEMO_WORD      : TEST_DEMO_WORD,
    TestDemoBlank       : TestDemoBlank,
    TestDemoEnd         : TestDemoEnd,
    TestDemoStart       : TestDemoStart,
    TestDemoWord        : TestDemoWord
}