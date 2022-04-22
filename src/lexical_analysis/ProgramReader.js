
//程序阅读器，解析一段程序，获取到每个字符的行列值
//支持迭代获取和重置，配合语法解析器使用
class ProgramReader{

    constructor(program){
        this.init(program + '\0')
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
        this.length = program.length
        this.content = []

        let line = 1
        let col = 0
        for(let i = 0;i < this.length;i++){
            col++
            this.content[i] = {
                char    : program[i],
                line    : line,
                col     : col
            }
            if(program[i] == '\n'){
                line++
                this.lines = line
                col = 0
            }
        }
    }

    getLines(){
        return this.lines
    }

    getCol(){
        return this.col
    }
    
    hasNextChar(){
        return this.currIdx < this.program.length
    }

    getNextChar(){
        if(!this.hasNextChar()){
            return null
        }
        this.currIdx ++
        return this.content[this.currIdx - 1]
    }


    goback(k){
        this.currIdx = Math.max(0,this.currIdx - k)
    }
}
module.exports = ProgramReader