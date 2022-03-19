var pathTool = require('path')
var fs = require('fs')

exports.LoadSourceCode = function(filename){
    let path = __dirname + '/' + filename
    
    return fs.readFileSync(path).toString()
}

exports.SaveTokens = function(filename,tokens){
    let path = pathTool.resolve(__dirname,'../../outputs') + '/' + filename
    console.log(path)
    let content = JSON.stringify(tokens)

    fs.writeFileSync(path,content)
}

exports.SaveLogs = function(filename,logs){

}
