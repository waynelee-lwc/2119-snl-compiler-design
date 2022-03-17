
var models = require('./models')

/**
 * tokens文件，存放编译过程中可能遇到的各种类型token
 * 在这个文件里面命名token类型和实现工厂方法
 */

exports.ID_TOKEN_TYPE = "ID"
exports.RESERVED_TOKEN_TYPE = "RESERVED"
exports.NUMBER_TOKEN_TYPE = "NUMBER"

exports.GetToken = function(type,name,line,col){
    return new models.Token(type,name,line,col)
}

/**
 * 测试程序会生成的token类型
 */
exports.TEST_DEMO_WORD_TOkEN_TYPE = "WORD"

exports.TEST_DEMO_BLANK_TOKEN_TYPE = "BLANK"

exports.TEST_DEMO_END_TOKEN_TYPE = "END"

exports.TEST_DEMO_RESERVED_TOKEN_TYPE = "RESERVED"
//...