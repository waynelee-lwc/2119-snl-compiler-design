var models = require('./models')

export const ID_TOKEN_TYPE = "ID"
export const RESERVED_TOKEN_TYPE = "RESERVED"
export const NUMBER_TOKEN_TYPE = "NUMBER"


export function ID(name,line,col){
    return models.Token(ID_TOKEN_TYPE,name,line,col)
}

export function Reserved(name,line,col){
    return models.Token(RESERVED_TOKEN_TYPE,name,line,col)
}

export function Number(name,line,col){
    return models.Token(NUMBER_TOKEN_TYPE,name,line,col)
}

export function Seperator(name,line,col){
    
}
//...