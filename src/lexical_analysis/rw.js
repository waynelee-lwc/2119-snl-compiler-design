var pathTool = require('path')
var fs = require('fs')

exports.LoadSourceCode = function(filename){
    
    return fs.readFileSync(filename).toString()
}

exports.Save = function(filename,tokens){
    let path = pathTool.resolve(filename)
    // console.log(path)
    let content = JSON.stringify(tokens)

    fs.writeFileSync(path,content)
}

exports.Loads = function(filename){
    let path = pathTool.resolve(filename)
    return fs.readFileSync(path)
}
