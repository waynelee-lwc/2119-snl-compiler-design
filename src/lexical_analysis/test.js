
var dict = require('./dict')
var checking = require('./checking')
var rw = require('./rw')
var model = require('./model')

// console.log(dict.LegalCharacter['a'])
// console.log(checking.IsLegal('a'))
// console.log(checking.IsLowerLetter)

// console.log(rw.LoadSourceCode('readingtest.txt').split('\n'))
// console.log(__dirname)

// var token = new model.Token('testtype','testname',13)

// console.log(JSON.stringify(token))

let code = rw.LoadSourceCode('readingtest.txt').split('\n')
for(idx in code){
    console.log(Number(idx) + 1,code[idx])
}