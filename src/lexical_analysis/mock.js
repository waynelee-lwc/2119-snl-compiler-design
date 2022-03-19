var tokens = require('./model/tokens')
var rw = require('./rw')

/**
 * Mock一个测试用例
 */

let tokenList = []

tokenList.push(tokens.GetToken(tokens.RESERVED  ,'program'  ,1,1))
tokenList.push(tokens.GetToken(tokens.ID        ,'p'        ,1,1))

tokenList.push(tokens.GetToken(tokens.RESERVED  ,'type'     ,2,1))
tokenList.push(tokens.GetToken(tokens.ID        ,'t1'       ,2,1))
tokenList.push(tokens.GetToken(tokens.SEPERATOR ,'='        ,2,1))
tokenList.push(tokens.GetToken(tokens.RESERVED  ,'integer'  ,2,1))
tokenList.push(tokens.GetToken(tokens.SEPERATOR ,';'        ,2,1))

tokenList.push(tokens.GetToken(tokens.RESERVED  ,'val'      ,3,1))
tokenList.push(tokens.GetToken(tokens.RESERVED  ,'integer'  ,3,1))
tokenList.push(tokens.GetToken(tokens.ID        ,'v1'       ,3,1))
tokenList.push(tokens.GetToken(tokens.SEPERATOR ,','        ,3,1))
tokenList.push(tokens.GetToken(tokens.ID        ,'v2'       ,3,1))
tokenList.push(tokens.GetToken(tokens.SEPERATOR ,';'        ,3,1))

tokenList.push(tokens.GetToken(tokens.RESERVED  ,'procedure',4,1))
tokenList.push(tokens.GetToken(tokens.ID        ,'q'        ,4,1))
tokenList.push(tokens.GetToken(tokens.SEPERATOR ,'('        ,4,1))
tokenList.push(tokens.GetToken(tokens.RESERVED  ,'integer'  ,4,1))
tokenList.push(tokens.GetToken(tokens.ID        ,'i'        ,4,1))
tokenList.push(tokens.GetToken(tokens.SEPERATOR ,')'        ,4,1))
tokenList.push(tokens.GetToken(tokens.SEPERATOR ,';'        ,4,1))

tokenList.push(tokens.GetToken(tokens.RESERVED  ,'var'      ,5,1))
tokenList.push(tokens.GetToken(tokens.RESERVED  ,'integer'  ,5,1))
tokenList.push(tokens.GetToken(tokens.ID        ,'a'        ,5,1))
tokenList.push(tokens.GetToken(tokens.SEPERATOR ,';'        ,5,1))


tokenList.push(tokens.GetToken(tokens.RESERVED  ,'begin'    ,6,1))

tokenList.push(tokens.GetToken(tokens.ID        ,'a'        ,7,1))
tokenList.push(tokens.GetToken(tokens.ASSIGN    ,':='       ,7,1))
tokenList.push(tokens.GetToken(tokens.ID        ,'i'        ,7,1))
tokenList.push(tokens.GetToken(tokens.SEPERATOR ,';'        ,7,1))

tokenList.push(tokens.GetToken(tokens.RESERVED  ,'write'    ,8,1))
tokenList.push(tokens.GetToken(tokens.SEPERATOR ,'('        ,8,1))
tokenList.push(tokens.GetToken(tokens.ID        ,'a'        ,8,1))
tokenList.push(tokens.GetToken(tokens.SEPERATOR ,')'        ,8,1))

tokenList.push(tokens.GetToken(tokens.RESERVED  ,'end'      ,9,1))


tokenList.push(tokens.GetToken(tokens.RESERVED  ,'begin'    ,10,1))


tokenList.push(tokens.GetToken(tokens.RESERVED  ,'read'     ,11,1))
tokenList.push(tokens.GetToken(tokens.SEPERATOR ,'('        ,11,1))
tokenList.push(tokens.GetToken(tokens.ID        ,'v1'       ,11,1))
tokenList.push(tokens.GetToken(tokens.SEPERATOR ,'('        ,11,1))
tokenList.push(tokens.GetToken(tokens.SEPERATOR ,';'        ,11,1))

tokenList.push(tokens.GetToken(tokens.RESERVED  ,'if'       ,12,1))
tokenList.push(tokens.GetToken(tokens.ID        ,'v1'       ,12,1))
tokenList.push(tokens.GetToken(tokens.SEPERATOR ,'<'        ,12,1))
tokenList.push(tokens.GetToken(tokens.NUMBER    ,'10'       ,12,1))
tokenList.push(tokens.GetToken(tokens.RESERVED  ,'then'     ,12,1))
tokenList.push(tokens.GetToken(tokens.ID        ,'v1'       ,12,1))
tokenList.push(tokens.GetToken(tokens.ASSIGN    ,':='       ,12,1))
tokenList.push(tokens.GetToken(tokens.ID        ,'v1'       ,12,1))
tokenList.push(tokens.GetToken(tokens.SEPERATOR ,'+'        ,12,1))
tokenList.push(tokens.GetToken(tokens.NUMBER    ,'10'       ,12,1))
tokenList.push(tokens.GetToken(tokens.RESERVED  ,'else'     ,12,1))
tokenList.push(tokens.GetToken(tokens.ID        ,'v1'       ,12,1))
tokenList.push(tokens.GetToken(tokens.ASSIGN    ,':='       ,12,1))
tokenList.push(tokens.GetToken(tokens.ID        ,'v1'       ,12,1))
tokenList.push(tokens.GetToken(tokens.SEPERATOR ,'-'        ,12,1))
tokenList.push(tokens.GetToken(tokens.NUMBER    ,'10'       ,12,1))
tokenList.push(tokens.GetToken(tokens.RESERVED  ,'fi'       ,12,1))
tokenList.push(tokens.GetToken(tokens.SEPERATOR ,';'        ,12,1))

tokenList.push(tokens.GetToken(tokens.ID        ,'q'        ,13,1))
tokenList.push(tokens.GetToken(tokens.SEPERATOR ,'('        ,13,1))
tokenList.push(tokens.GetToken(tokens.ID        ,'v1'       ,13,1))
tokenList.push(tokens.GetToken(tokens.SEPERATOR ,')'        ,13,1))

tokenList.push(tokens.GetToken(tokens.RESERVED  ,'end'      ,14,1))

tokenList.push(tokens.GetToken(tokens.SEPERATOR ,'.'        ,15,1))

tokenList.push(tokens.GetToken(tokens.EOF       ,'EOF'      ,16,1))

console.log(tokenList.length)
rw.SaveTokens("mock_tokens.txt",tokenList)
