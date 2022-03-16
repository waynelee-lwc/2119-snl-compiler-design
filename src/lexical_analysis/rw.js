
var fs = require('fs')

exports.LoadSourceCode = function(filename){
    let path = __dirname + '/' + filename
    
    return fs.readFileSync(path).toString()
}

exports.SaveTokens = function(filename,tokens){

}

exports.SaveLogs = function(filename,logs){

}
