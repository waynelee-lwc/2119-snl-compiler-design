var pathTool = require('path')
var fs = require('fs')

exports.LoadSourceCode = function(filename){
    let path = __dirname + '/' + filename
    
    return fs.readFileSync(path).toString()
}

exports.Save = function(filename,tokens){
    let path = pathTool.resolve(__dirname,filename)
    // console.log(path)
    let content = JSON.stringify(tokens)

    fs.writeFileSync(path,content)
}

exports.SaveLogs = function(filename,logs){

}

exports.Loads = function(filename){
    let path = pathTool.resolve(__dirname,filename)
    return fs.readFileSync(path)
}
