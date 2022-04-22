
/*
    字典文件，存放各种对照表
    map,正则表达式
    用哪个实现哪个
*/
//字母
exports.LetterReg = /[a-zA-Z]/
//小写字母
exports.LowerLetterReg = /[a-z]/
exports.LowerLetter = {}
//大写字母
exports.UpperLetterReg = /[A-Z]/
exports.UpperLetter = {}
//数字
exports.NumberReg = /[0-9]/
exports.Number = {}
//非0数字
exports.NonZeroNumberReg = /[1-9]/
exports.NonZeroNumber = {}
//分界符
exports.SeperatorReg = / /
exports.Seperator = []
exports.SeperatorList = '+-*/();[]=<,'
//点符
exports.DotReg = /\./
//等号
exports.EqualSignReg = /\=/
//合法字符
exports.LegalCharacterReg = /[0-9a-zA-z]/
exports.LegalCharacter = {}
exports.LegalCharacterList = `+-*/<=()[]{}.',;: \n\0\t`
//保留字
exports.ReservedReg = / /
exports.Reserved = ['program','procedure','type','var','if','then','else','fi','while','do','endwh','begin','end','read','write','array','of','record','return','integer','char']
//无符号整数
exports.UnsignedIntegerReg = /[1-9][0-9]?/
exports.UnsignedInteger = {}
//注释头符
exports.CommentHeaderReg = /\{/
//注释尾符
exports.CommentEnderReg = /\}/
//空白字符
exports.Blank = ' \n\t'
//冒号
exports.ColonReg = /\:/
//单引号
exports.ApostropheReg = /\'/
//EOF
exports.EOFList = ['\0'] 