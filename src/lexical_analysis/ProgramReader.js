
//程序阅读器，解析每一个字符，获取行列值
export class ProgramReader{

    constructor(program){
        this.init(program)
    }

    init(program){
        this.setProgram(program)
        this.reset()
    }

    reset(){
        this.col = 1
        this.line = 1
        this.currIdx = 0
    }

    setProgram(program){
        this.program = program
    }

    getLine(){
        return this.line
    }

    getCol(){
        return this.line
    }
    
    hasNextChar(){
        return this.currIdx < this.program.length
    }

    getNextChar(){
        if(!this.hasNextChar()){
            return null
        }
        ch = this.program[this.currIdx]
        this.currIdx += 1
        this.col++

        resp = {
            char : ch,
            line : this.line,
            col  : this.col
        }

        if(ch == '\n'){
            this.line ++
            this.col = 1
        }
        return resp
    }
}