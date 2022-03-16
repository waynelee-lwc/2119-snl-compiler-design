
/*
    字典文件，存放各种对照表
    map,正则表达式
    用哪个实现哪个
*/
//字母
exports.LetterReg = /[a-z,A-Z]/
//小写字母
exports.LowerLetterReg = /[a-z]/
exports.LowerLetter = {

}
//大写字母
exports.UpperLetterReg = /[A-Z]/
exports.UpperLetter = {

}
//数字
exports.NumberReg = /[0-9]/
exports.Number = {

}
//非0数字
exports.NonZeroNumberReg = /[1-9]/
exports.NonZeroNumber = {

}
//分界符
exports.SeperatorReg = / /
exports.Seperator = {

}
//符号集合
exports.SymbolReg = / /
exports.Symbol = {

}
//合法字符
exports.LegalCharacterReg = / /
exports.LegalCharacter = {

}
//保留字
exports.ReservedReg = / /
exports.Reserved = {    //map或者list都可以，map更快一些，list更好写一些
    'program':true,
    'if':true,
    'else':true
    //...
}
//无符号整数
exports.UnsignedIntegerReg = /[1-9][0-9]?/
exports.UnsignedInteger = {

}
//程序结束符
exports.ProgramEnderReg = / /
exports.ProgramEnder = {
    '.':true
}
