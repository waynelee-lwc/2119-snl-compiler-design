
var dict = require('./dict')
var checking = require('./checking')
var rw = require('./rw')
var model = require('./model/models')
var ProgramReader = require('./ProgramReader')
var tokens = require('./model/tokens')

// console.log(dict.LegalCharacter['a'])
// console.log(checking.IsLegal('a'))
// console.log(checking.IsLowerLetter)

// console.log(rw.LoadSourceCode('readingtest.txt').split('\n'))
// console.log(__dirname)

// var token = new model.Token('testtype','testname',13)

// console.log(JSON.stringify(token))

// let code = rw.LoadSourceCode('readingtest.txt').split('\n')
// for(idx in code){
//     console.log(Number(idx) + 1,code[idx])
// }

// let endState = new model.StateVertex(
//     'end',
//     function(ch){
//         let res = {
//             error       : null,
//             tokenEnd    : false,
//             nextState   : this,
//             log         : null,
//             parseEnd    : true
//         }

//         this.tokenStr += ch
//         this.endCol ++
//         res.log = new model.Log(this.line,this.endCol,`parse char : ${ch}`)
//         return res
//     },
//     function(){
//         return new model.Token('program end','.',this.line,`${this.beginCol}-${this.endCol}`)
//     }
// )
// let beginState = new model.StateVertex(
//     'begin',
//     function(ch){
//         let res = {
//             error       : null,
//             tokenEnd    : false,
//             nextState   : this,
//             log         : null,
//             parseEnd    : false
//             //TODO hastoken
//         }

//         if(checking.IsLetter(ch)){
//             res.tokenEnd = true
//             res.nextState = testState
//             res.goback = true
//         }

//         return res
//     },
//     function(){

//     }
// )

// let testState = new model.StateVertex(
//     'test',
//     function(ch){
//         let res = {
//             error       : null,
//             tokenEnd    : false,
//             nextState   : this,
//             log         : null,
//             parseEnd    : false,
//             goback      : false
//         }
//         //非法字符
//         if(!checking.IsLegal(ch)){
//             res.error = new model.Error(this.line,this.endCol,`illegal character : ${ch}`)
//             res.state = null
//             return res
//         }
//         //程序结束符号
//         if(checking.IsProgramEnder(ch)){
//             res.tokenEnd = true
//             res.nextState = endState
//             res.goback = true
//             return res
//         }
//         //空格符号
//         if(checking.IsBlankSpace(ch)){
//             res.tokenEnd = true
//             res.nextState = beginState
//             res.goback = false
//             return res
//         }

//         this.tokenStr += ch
//         this.endCol ++
//         res.log = new model.Log(this.line,this.endCol,`parse char :${ch}`)
        

//         return res
//     },
//     function(){
//         return new model.Token('test',this.tokenStr,this.line,`${this.beginCol}-${this.endCol}`)
//     }
// )

// let testStr = 'hello world from nodejs.'
// let tokenList = []

// let currState = beginState
// currState.init(1,1)
// for(let i = 0;i < testStr.length;i++){
//     res = currState.parse(testStr[i])
//     if(res.error != null){
//         break;
//     }
//     if(res.tokenEnd){
//         token = currState.getToken()
//         if(token){
//             console.log('token:',JSON.stringify(token))
//             tokenList.push(token)
//         }
//         currState = res.nextState
//         currState.init(1,Number(i) + 1)
//         i -= res.goback ? 1 : 0
//     }else{
//         console.log('res  :',JSON.stringify(res.log))
//     }
//     if(res.parseEnd){
//         break;
//     }
// }

// console.log(tokenList)

let str = 'testing \
hello world. \n \
haha'

program = rw.LoadSourceCode('./readingtest.txt')
reader = new ProgramReader(program)

while(reader.hasNextChar()){
    console.log(reader.getNextChar())
}

console.log(tokens.ID_TOKEN_TYPE)
console.log(tokens.RESERVED_TOKEN_TYPE)