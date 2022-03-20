var models = require('./models')

//非法字符
exports.IllegalCharacterError = function(ch){return new models.Error(`illegal character '${ch}'`)}
//解析冒号出错
exports.ErrorNextColon        = function(ch){return new models.Error(`error next color ${ch}`)}
//解析字符串出错
exports.ErrorInChar           = function(ch){return new models.Error(`error when parsing a char ${ch}`)}
//未定义错误
exports.UndefinedError        = function(ch){return new models.Error(`caught an undefined error ! ${ch}`)}
//程序不完整
exports.NeedDot               = function(){return new models.Error(`need a dot at the end of program!`)}
//...