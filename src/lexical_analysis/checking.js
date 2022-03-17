
/* 
    校验检测部分代码
*/
var dict = require('./dict')

/* 单字符检测 */
//合法字符
exports.IsLegal = (ch)=>{
    return true
}
//数字
exports.IsNumber = (ch)=>{
    
}
//非0数字
exports.IsNonZeroNumber = (ch)=>{

}
//字母
exports.IsLetter = (ch)=>{
    return dict.LetterReg.test(ch)
}
//小写字母
exports.IsLowerLetter = (ch)=>{

}
//大写字母
exports.IsUpperLetter = (ch)=>{

}
//分界符
exports.IsSeperator = (ch)=>{

}
//字符起始结束符
exports.IsCharacterMarker = (ch)=>{

}
//程序结束符
exports.IsProgramEnder = (ch)=>{
    return dict.ProgramEnder[ch]
}
//是否空格
exports.IsBlankSpace = (ch)=>{
    return ch === ' '
}

/* token类型检测 */
//合法ID
exports.IsLegalID = (token)=>{

}
//无符号整数
exports.IsUnsignedInteger = (token)=>{

}
//保留字
exports.IsReserved = (token)=>{
    return dict.Reserved[token]
}
//单字符分界符
exports.IsSingleSeperator = (token)=>{

}
//双字符分界符号
exports.IsDoubleSeperator = (token)=>{

}
//注释头符
exports.IsCommentHeader = (token)=>{

}
//注释尾符
exports.IsCommentEnder = (token)=>{

}
//数组下标界限符
exports.IsArrayIndexRange = (token)=>{

}
