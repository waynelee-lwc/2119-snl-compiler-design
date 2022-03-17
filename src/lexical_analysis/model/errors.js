var models = require('./models')

//非法字符
exports.IllegalCharacterError = function(ch){return new models.Error(`illegal character '${ch}'`)}
//...