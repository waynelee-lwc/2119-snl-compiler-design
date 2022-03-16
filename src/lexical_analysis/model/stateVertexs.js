
export const endState = new model.StateVertex(
    'end',
    function(ch){
        let res = {
            error       : null,
            tokenEnd    : false,
            nextState   : this,
            log         : null,
            parseEnd    : true
        }

        this.tokenStr += ch
        this.endCol ++
        res.log = new model.Log(this.line,this.endCol,`parse char : ${ch}`)
        return res
    },
    function(){
        return new model.Token('program end','.',this.line,`${this.beginCol}-${this.endCol}`)
    }
)

export const  beginState = new model.StateVertex(
    'begin',
    function(ch){
        let res = {
            error       : null,
            tokenEnd    : false,
            nextState   : this,
            log         : null,
            parseEnd    : false
            //TODO hastoken
        }

        if(checking.IsLetter(ch)){
            res.tokenEnd = true
            res.nextState = testState
            res.goback = true
        }

        return res
    },
    function(){

    }
)

export const testState = new model.StateVertex(
    'test',
    function(ch){
        let res = {
            error       : null,
            tokenEnd    : false,
            nextState   : this,
            log         : null,
            parseEnd    : false,
            goback      : false
        }
        //非法字符
        if(!checking.IsLegal(ch)){
            res.error = new model.Error(this.line,this.endCol,`illegal character : ${ch}`)
            res.state = null
            return res
        }
        //程序结束符号
        if(checking.IsProgramEnder(ch)){
            res.tokenEnd = true
            res.nextState = endState
            res.goback = true
            return res
        }
        //空格符号
        if(checking.IsBlankSpace(ch)){
            res.tokenEnd = true
            res.nextState = beginState
            res.goback = false
            return res
        }

        this.tokenStr += ch
        this.endCol ++
        res.log = new model.Log(this.line,this.endCol,`parse char :${ch}`)
        

        return res
    },
    function(){
        return new model.Token('test',this.tokenStr,this.line,`${this.beginCol}-${this.endCol}`)
    }
)