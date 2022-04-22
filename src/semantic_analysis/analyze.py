# initialize global
global LOG, TAG, DEBUG, mainOff, Off, savedOff

from symbTable import *
from globals import Log
import sys

Off = 0
Level = -1
scope = [None] * SCOPESIZE
intPtr = None
charPtr = None
boolPtr = None


def initialize():
    global scope, intPtr, charPtr, boolPtr
    intPtr = NewTy(TypeKind.intTy)
    charPtr = NewTy(TypeKind.charTy)
    boolPtr = NewTy(TypeKind.boolTy)


def TypeProcess(t, deckind):
    Ptr = None
    if deckind == DecKind.IdK:
        Ptr = nameType(t)
    elif deckind == DecKind.ArrayK:
        Ptr = arrayType(t)
    elif deckind == DecKind.RecordK:
        Ptr = recordType(t)
    elif deckind == DecKind.IntegerK:
        Ptr = intPtr
    elif deckind == DecKind.CharK:
        Ptr = charPtr

    return Ptr


def nameType(t):
    Ptr = None
    entry = None
    present, entry = FindEntry(t.attr['type_name'], entry)

    if present == True:
        if entry.attrIR.kind != IdKind.typeKind:
            ErrorPrompt(t.linePos, t.attr['type_name'], "used before typed!\n")
        else:
            Ptr = entry.attrIR.idtype

    else:
        ErrorPrompt(t.linePos, t.attr['type_name'], "type name is not declared!\n")

    return Ptr


def arrayType(t):
    ptr0 = None
    ptr1 = None
    ptr = None
    if t.attr['ArrayAttr']['low'] > t.attr['ArrayAttr']['up']:
        ErrorPrompt(t.linePos, "", "array subscript error!\n")
        Error = True

    else:
        ptr0 = TypeProcess(t, DecKind.IntegerK)
        ptr1 = TypeProcess(t, t.attr['ArrayAttr']['childtype'])
        ptr = NewTy(TypeKind.arrayTy)
        ptr.size = (t.attr['ArrayAttr']['up'] - t.attr['ArrayAttr']['low'] + 1) * ptr1.size

        ptr.More['ArrayAttr']['indexTy'] = ptr0
        ptr.More['ArrayAttr']['elemTy'] = ptr1
        ptr.More['ArrayAttr']['low'] = t.attr['ArrayAttr']['low']
        ptr.More['ArrayAttr']['up'] = t.attr['ArrayAttr']['up']

    return ptr


def recordType(t):
    Ptr = NewTy(TypeKind.recordTy)
    t = t.child[0]

    Ptr2 = None
    Ptr1 = None
    body = None

    while t != None:
        i = 0
        while i < t.idnum:
            Ptr2 = NewBody()
            if body == None:
                body = Ptr1 = Ptr2

            t.name[i] = Ptr2.id
            Ptr2.UnitType = TypeProcess(t, t.kind['dec'])

            Ptr2.Next = None

            if Ptr2 != Ptr1:
                Ptr2.off = Ptr1.off + Ptr1.UnitType.size
                Ptr1.Next = Ptr2
                Ptr1 = Ptr2
            i += 1

        t = t.brother
    Ptr.size = Ptr2.off + Ptr2.UnitType.size
    Ptr.More['body'] = body
    return Ptr


def TypeDecPart(t):
    present = False
    entry = None

    attrIr = AttributeIR()
    attrIr.kind = IdKind.typeKind
    while t != None:

        present, attrIr, entry = Enter(t.name[0], attrIr, entry)
        if present != False:
            ErrorPrompt(t.linePos, t.name[0], "is repetation declared!\n")
            entry = None
        else:
            entry.attrIR.idtype = TypeProcess(t, t.kind['dec'])
        t = t.brother


def varDecPart(t):
    VarDecList(t)


def VarDecList(t):
    global mainOff, savedOff, Off, Level
    attrIr = AttributeIR()
    present = False
    entry = None

    while t != None:
        attrIr.kind = IdKind.varKind
        i = 0
        while i < t.idnum:
            attrIr.idtype = TypeProcess(t, t.kind['dec'])

            if t.attr['ProcAttr']['paramt'] == ParamType.varparamType:
                attrIr.More['VarAttr']['access'] = AccessKind.indir
                attrIr.More['VarAttr']['level'] = Level

                attrIr.More['VarAttr']['off'] = Off
                Off += 1

            else:
                attrIr.More['VarAttr']['access'] = AccessKind.dir
                attrIr.More['VarAttr']['level'] = Level

                if attrIr.idtype != None:
                    attrIr.More['VarAttr']['off'] = Off
                    Off = Off + attrIr.idtype.size

            present, attrIr, entry = Enter(t.name[i], attrIr, entry)
            if present != False:
                ErrorPrompt(t.linePos, t.name[i], " is defined repetation!\n")
            else:
                t.table[i] = entry

            i += 1

        if t != None:
            t = t.brother

    if Level == 0:
        mainOff = Off
        StoreNoff = Off
    else:
        savedOff = Off


def procDecPart(t):
    global Level
    p = t
    entry = HeadProcess(t)

    #遍历定义节点
    t = t.child[1]
    while t != None:
        if t.nodeKind == NodeKind.TypeK:#类型定义节点
            TypeDecPart(t.child[0])
            return
        elif t.nodeKind == NodeKind.VarK:#变量定义节点
            varDecPart(t.child[0])
        elif t.nodeKind == NodeKind.ProcDecK:
            break
        else:
            ErrorPrompt(t.linePos, "", "no this node kind in syntax tree!")

        # if t.nodeKind == NodeKind.ProcDecK:
        #     break
        # else:
        t = t.brother

    entry.attrIR.More['ProcAttr']['nOff'] = savedOff
    entry.attrIR.More['ProcAttr']['mOff'] = entry.attrIR.More['ProcAttr']['nOff'] + entry.attrIR.More['ProcAttr'][
        'level'] + 1
    #处理过程定义
    while t != None:
        procDecPart(t)
        t = t.brother

    t = p
    Body(t.child[2])
    if Level != -1:
        DestroyTable()


#过程定义头处理
def HeadProcess(t):
    global Level

    #创建过程
    attrIr = AttributeIR()
    present = False
    entry = None

    attrIr.kind = IdKind.procKind
    attrIr.idtype = None
    attrIr.More['ProcAttr']['level'] = Level + 1

    if t != None:
        present, attrIr, entry = Enter(t.name[0], attrIr, entry)
        t.table[0] = entry

    entry.attrIR.More['ProcAttr']['param'] = ParaDecList(t)
    return entry


def ParaDecList(t):
    global Level, Off

    p = None
    Ptr1 = None
    Ptr2 = None
    head = None

    if t != None:
        if t.child[0] != None:
            p = t.child[0]
        Level, Off = CreatTable()
        Off = 7
        varDecPart(p)
        Ptr0 = scope[Level]

        while Ptr0 != None:
            Ptr2 = NewParam()
            if head == None:
                head = Ptr1 = Ptr2
            Ptr2.entry = Ptr0
            Ptr2.next = None

            if Ptr2 != Ptr1:
                Ptr1.next = Ptr2
                Ptr1 = Ptr2

            Ptr0 = Ptr0.next

    return head


def Body(t):
    if t.nodeKind == NodeKind.StmLK:
        p = t.child[0]
        while p != None:
            statement(p)
            p = p.brother


def statement(t):
    if t.kind['stmt'] == StmtKind.IfK:
        ifstatement(t)
    elif t.kind['stmt'] == StmtKind.WhileK:
        whilestatement(t)
    elif t.kind['stmt'] == StmtKind.AssignK:
        assignstatement(t)
    elif t.kind['stmt'] == StmtKind.ReadK:
        readstatement(t)
    elif t.kind['stmt'] == StmtKind.WriteK:
        writestatement(t)
    elif t.kind['stmt'] == StmtKind.CallK:
        callstatement(t)
    elif t.kind['stmt'] == StmtKind.ReturnK:
        returnstatement(t)
    else:
        ErrorPrompt(t.linePos, "", "statement type error!\n")


def expr(t, Ekind):
    present = False
    entry = None

    Eptr0 = None
    Eptr1 = None
    Eptr = None
    if t != None:
        if t.kind['exp'] == ExpKind.ConstK:
            Eptr = TypeProcess(t, DecKind.IntegerK)
            Eptr.kind = TypeKind.intTy
            if Ekind != None:
                Ekind = AccessKind.dir
        elif t.kind['exp'] == ExpKind.VariK:
            if t.child[0] == None:
                present, entry = FindEntry(t.name[0], entry)
                t.table[0] = entry

                if present != False:
                    if FindAttr(entry).kind != IdKind.varKind:
                        ErrorPrompt(t.linePos, t.name[0], "is not variable error!\n")
                        Eptr = None
                    else:
                        Eptr = entry.attrIR.idtype
                        if Ekind != None:
                            Ekind = AccessKind.indir

                else:
                    ErrorPrompt(t.linePos, t.name[0], "is not declarations!\n")

            else:
                if t.attr['ExpAttr']['varkind'] == VarKind.ArrayMembV:
                    Expr = arrayVar(t)
                else:
                    if t.attr['ExpAttr']['varkind'] == VarKind.FieldMembV:
                        Expr = recordVar(t)

        elif t.kind['exp'] == ExpKind.OpK:
            Eptr0 = expr(t.child[0], None)
            if Eptr0 == None:
                return None
            Eptr1 = expr(t.child[1], None)
            if Eptr1 == None:
                return None

            present = Compat(Eptr0, Eptr1)
            if present != False:
                if t.attr['ExpAttr']['op'] == LexType.EQ:
                    Eptr = boolPtr
                elif t.attr['ExpAttr']['op'] == LexType.OVER:
                    Eptr = intPtr

                if Ekind != None:
                    Ekind = AccessKind.dir

            else:
                ErrorPrompt(t.linePos, "", "operator is not compat!\n")

    return Eptr


def arrayVar(t):
    present = False
    entry = None

    Eptr0 = None
    Eptr1 = None
    Eptr = None

    present, entry = FindEntry(t.name[0], entry)
    t.table[0] = entry

    if present == False:
        if FindAttr(entry).kind != IdKind.varKind:
            ErrorPrompt(t.linePos, t.name[0], "is not variable error!\n")
            Eptr = None

        else:
            if FindAttr(entry).idtype.kind != TypeKind.arrayTy:
                ErrorPrompt(t.linePos, t.name[0], "is not array variable error !\n")
                Eptr = None

            else:
                Eptr0 = entry.attrIR.idtype.More.ArrayAttr.indexTy
                if Eptr0 == None:
                    return None
                Eptr1 = expr(t.child[0], None)
                if Eptr1 == None:
                    return None
                present = Compat(Eptr0, Eptr1)
                if present != True:
                    ErrorPrompt(t.linePos, "", "type is not matched with the array member error !\n")
                    Eptr = None
                else:
                    Eptr = entry.attrIR.idtype.More.ArrayAttr.elemTy

    else:
        ErrorPrompt(t.linePos, t.name[0], "is not declarations!\n")
    return Eptr


def recordVar(t):
    present = False
    result = True
    entry = None

    Eptr0 = None
    Eptr1 = None
    Eptr = None
    currentP = None

    present, entry = FindEntry(t.name[0], entry)
    t.table[0] = entry

    if present != False:
        if FindAttr(entry).idtype.kind != IdKind.varKind:
            ErrorPrompt(t.linePos, t.name[0], "is not variable error!\n")
            Eptr = None

        else:
            if FindAttr(entry).idtype.kind != TypeKind.recordTy:
                ErrorPrompt(t.linePos, t.name[0], "is not record variable error !\n")
                Eptr = None

            else:
                Eptr0 = entry.attrIR.idtype
                currentP = Eptr0.More.body
                while currentP != None and result != False:
                    result = (t.child[0].name[0] == currentP.id)
                    if result == False:
                        Eptr = currentP.UnitType
                    else:
                        currentP = currentP.Next

                if currentP == None:
                    if result != False:
                        ErrorPrompt(t.child[0].linePos, t.child[0].name[0], "is not field type!\n")
                        Eptr = arrayVar(t.child[0])

    else:
        ErrorPrompt(t.linePos, t.name[0], "is not declarations!\n")
    return Eptr


def assignstatement(t):
    entry = None

    present = False
    ptr = None
    Eptr = None

    child1 = None
    child2 = None

    child1 = t.child[0]
    child2 = t.child[1]

    if child1.child[0] == None:
        present, entry = FindEntry(child1.name[0], entry)

        if present != False:
            if FindAttr(entry).kind != IdKind.varKind:
                ErrorPrompt(child1.lineon, child1.name[0], "is not variable error!\n")
                Eptr = None

            else:
                Eptr = entry.attrIR.idtype
                child1.table[0] = entry

        else:
            ErrorPrompt(child1.lineon, child1.name[0], "is not declarations!\n")

    else:
        if child1.attr['ExpAttr']['varkind'] == VarKind.ArrayMembV:
            Eptr = arrayVar(child1)
        else:
            if child1.attr['ExpAttr']['varkind'] == VarKind.FieldMembV:
                Eptr = recordVar(child1)

    if Eptr != None:
        if t.nodeKind == NodeKind.StmLK and t.kind['stmt'] == StmtKind.AssignK:
            ptr = expr(child2, None)
            if Compat(ptr, Eptr):
                pass
            else:
                ErrorPrompt(t.linePos, "", "ass_expression error!\n")


def callstatement(t):
    Ekind = AccessKind
    present = False
    entry = None

    present, entry = FindEntry(t.child[0].name[0], entry)
    t.child[0].table[0] = entry

    if present == False:
        ErrorPrompt(t.linePos, t.chlid[0].name[0], "function is not declarationed!\n")

    else:
        if FindAttr(entry).kind != IdKind.procKind:
            ErrorPrompt(t.linePos, t.name[0], "is not function name!\n")
        else:
            p = t.child[1]
            paramP = FindAttr(entry.More.ProcAttr.param)
            while p != None and paramP != None:
                paraEntry = paramP.entry
                Etp = expr(p, Ekind)
                if FindAttr(paraEntry).More.Varattr.access == AccessKind.indir and Ekind == AccessKind.dir:
                    ErrorPrompt(p.lineon, "", "param kind is not match!\n")
                else:
                    if FindAttr(paraEntry).idtype != Etp:
                        ErrorPrompt(p.lineon, "", "param type is not match!\n")

                p = p.brother
                paramP = paramP.next

            if p != None or paramP != None:
                ErrorPrompt(t.child[1].lineon, "", "param num is not match!\n")


def ifstatement(t):
    Ekind = None
    Etp = expr(t.child[0], Ekind)
    if Etp != None:
        if Etp.kind != TypeKind.boolTy:
            ErrorPrompt(t.linePos, "", "condition expressrion error!\n")
        else:
            p = t.child[1]
            while p != None:
                statement(p)
                p = p.brother

            t = t.child[2]

            while t != None:
                statement(t)
                t = t.brother


def whilestatement(t):
    Etp = expr(t.child[0], None)
    if Etp != None:
        if Etp.kind != TypeKind.boolTy:
            ErrorPrompt(t.linePos, "", "condition expression error!\n")
        else:
            t = t.child[1]
            while t != None:
                statement(t)
                t = t.brother


def readstatement(t):
    entry = None
    present = False

    present, entry = FindEntry(t.name[0], entry)
    t.table[0] = entry

    if present == False:
        ErrorPrompt(t.linePos, t.name[0], " is not declarationed!\n")
    else:
        if entry.attrIR.kind != IdKind.varKind:
            ErrorPrompt(t.linePos, t.name[0], "is not var name!\n ")


def writestatement(t):
    Etp = expr(t.child[0], None)
    if Etp != None:
        if Etp.kind == TypeKind.boolTy:
            ErrorPrompt(t.linePos, "", "exprssion type error!")


def returnstatement(t):
    global Level
    if Level == 0:
        ErrorPrompt(t.linePos, "", "return statement error!")

#分析主程序
def analyze(t):
    global Level, Off, LOG, TAG, Error
    entry = None
    p = None
    pp = t

    #创建新表格
    Level, Off = CreatTable()

    #初始化，放入默认类型
    initialize()

    #child0是phead，child1是定义节点
    p = t.child[1]

    #遍历定义节点
    while p != None:
        if p.nodeKind == NodeKind.TypeK:    #类型定义节点，先处理类型定义
            TypeDecPart(p.child[0])
        elif p.nodeKind == NodeKind.VarK:   #变量定义节点，先处理变量定义
            varDecPart(p.child[0])
        elif p.nodeKind == NodeKind.ProcDecK:#过程定义节点，节点本身需要处理
            procDecPart(p)
        else:
            ErrorPrompt(p.lineon, "", "no this node kind in syntax tree!")

        p = p.brother

    t = t.child[2]
    if t.nodeKind == NodeKind.StmtK:
        Body(t)

    if Level != -1:
        DestroyTable()

    if Error == True:
        LOG.e(DEBUG, "\nanalyze error:\n")
    else:
        pass
        #LOG.d(TAG, "\nanalyze has no error!\n")

if __name__ == '__main__':

    programDir = sys.argv[1] #代码产物文件夹
    # programDir = '/Users/bytedance/codes/jlu-2119-compiler-design/outputs/cache/2022-03-04_20:54:47_KACZQXNMDL'
    treePath = programDir + '/tree' #语法树输入
    semOutput = programDir + '/sem' #语义分析输出

    #重定向输出
    file = open(semOutput,'w')
    sys.stdout = file

    LOG = Log()
    TAG = "analyze.py"
    root1 = loadroot(treePath)
    analyze(root1)
    PrintSymbTable()
