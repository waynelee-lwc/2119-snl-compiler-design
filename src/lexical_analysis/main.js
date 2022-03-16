var ProgramReader = require('./ProgramReader').ProgramReader
var LexicalAnalysiser = require('./LexicalAnalysiser').LexicalAnalysiser
var rw = require('./rw')

function main(){

    let Program = rw.LoadSourceCode('readingtest.txt')
    reader = new ProgramReader(Program)
    parser = new LexicalAnalysiser(reader)
    resp = parser.parse()

    //error...

    //token list...

    //log list...
}

main()