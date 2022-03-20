
/* 
    校验检测代码
*/
var dict = require('./dict')

//合法字符
exports.IsLegal = (ch)=>{
    return dict.LegalCharacterReg.test(ch) || dict.LegalCharacterList.indexOf(ch) != -1
}
//数字
exports.IsNumber = (ch)=>{
    return dict.NumberReg.test(ch)
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
    return dict.SeperatorList.indexOf(ch) != -1
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
    return dict.Blank.indexOf(ch) != -1
}
//合法ID
exports.IsLegalID = (token)=>{

}
//无符号整数
exports.IsUnsignedInteger = (token)=>{

}
//保留字
exports.IsReserved = (token)=>{
    return dict.Reserved.indexOf(token) != -1
}
//注释头符
exports.IsCommentHeader = (ch)=>{
    return dict.CommentHeaderReg.test(ch)
}
//注释尾符
exports.IsCommentEnder = (token)=>{
    return dict.CommentEnderReg.test(ch)
}
//数组下标界限符
exports.IsArrayIndexRange = (token)=>{

}
//点符
exports.IsDot = (ch) =>{
    return dict.DotReg.test(ch)
}
//冒号
exports.IsColon = (ch) =>{
    return dict.ColonReg.test(ch)
}
//等号
exports.isEqualSign = (ch) =>{
    return dict.EqualSignReg.test(ch)
}
//单引号
exports.isApostrophe = (ch) =>{
    return dict.ApostropheReg.test(ch)
}
//EOF
exports.isEOF = (ch) =>{
    return dict.EOFList.indexOf(ch) != -1
}