'''
# 文件 symbTable.py
# 说明 语义分析，基于python实现
# 作者 yyq
'''

from globals import *
import analyze as analyze

LOG = Log()
TAG = "symbTbale.py"
DEBUG = "sym.py"
str1 = "ab2c"
str2 = "abc"

def printInLine(word):
    print(word, end="")

def PrintFieldChain(currentP):
    printInLine("\n--------------Field  chain--------------------\n")
    t = currentP

    while t != None:
        printInLine(t.id + ":  ")
        if t.UnitType.kind == TypeKind.intTy:
            LOG.d(TAG, "intTy     ")
        elif t.UnitType.kind == TypeKind.charTy:
            LOG.d(TAG, "charTy    ")
        elif t.UnitType.kind == TypeKind.arrayTy:
            LOG.d(TAG, "arrayTy   ")
        elif t.UnitType.kind == TypeKind.recordTy:
            LOG.d(TAG, "recordTy  ")
        else:
            LOG.e(DEBUG, "error type!  ")

        printInLine("off = " + t.off + "\n")
        t = t.Next


def PrintOneLayer(level):
    t = analyze.scope[level]
    printInLine("\n -------SymbTable in level " + str(level) + " ---------\n")
    while t != None:
        printInLine(t.idName + ":   ")
        Attrib = t.attrIR
        if Attrib.idtype != None:
            if Attrib.idtype.kind == TypeKind.intTy:
                printInLine("intTy  ")
            elif Attrib.idtype.kind == TypeKind.charTy:
                printInLine("charTy  ")
            elif Attrib.idtype.kind == TypeKind.arrayTy:
                printInLine("arrayTy  ")
            elif Attrib.idtype.kind == TypeKind.recordTy:
                printInLine("recordTy  ")
            else:
                printInLine("error type!  ")

        if Attrib.kind == IdKind.typeKind:
            printInLine("typekind  ")
        elif Attrib.kind == IdKind.varKind:
            printInLine("varkind  ")
            printInLine("Level = " + str(Attrib.More["VarAttr"]["level"]) + "  ")
            printInLine("Offset = " + str(Attrib.More["VarAttr"]["off"]) + "  ")
            if Attrib.More["VarAttr"]["access"] == AccessKind.dir:
                printInLine("dir  ")
            elif Attrib.More['VarAttr']['access'] == AccessKind.indir:
                printInLine("indir  ")
            else:
                printInLine("errorkind  ")
        elif Attrib.kind == IdKind.procKind:
            printInLine("funckind   ")
            printInLine("Level = " + str(Attrib.More["ProcAttr"]["level"]) + "  ")
            printInLine("Noff = " + str(Attrib.More["ProcAttr"]["nOff"]))
        else:
            printInLine("error  ")

        printInLine("\n")
        t = t.next


def PrintSymbTable():
    level = 0
    while analyze.scope[level] != None:
        PrintOneLayer(level)
        level += 1


def NewTable():
    table = Symbtable()

    table.next = None

    table.attrIR.kind = IdKind.typeKind
    table.attrIR.idtype = None
    table.next = None
    table.attrIR.More["VarAttr"]["isParam"] = False

    return table


def CreatTable():
    analyze.Level += 1
    analyze.scope[analyze.Level] = None
    analyze.Off = INITOFF
    return analyze.Level, analyze.Off


def DestroyTable():
    analyze.Level -= 1


def Enter(id, attribP, entry):
    present = False
    result = False
    curentry = analyze.scope[analyze.Level]
    prentry = analyze.scope[analyze.Level]

    if analyze.scope[analyze.Level] == None:
        curentry = NewTable()
        analyze.scope[analyze.Level] = curentry
    else:
        while curentry != None:
            prentry = curentry
            result = (id == curentry.idName)
            if result:
                LOG.e(DEBUG, "repetition declaration error !")
                Error = True
                present = True
                exit(-1)
            else:
                curentry = prentry.next

        if present == False:
            curentry = NewTable()
            prentry.next = curentry

    curentry.idName = id

    curentry.attrIR.idtype = attribP.idtype
    curentry.attrIR.kind = attribP.kind
    if attribP.kind == IdKind.typeKind:
        pass
    elif attribP.kind == IdKind.varKind:
        curentry.attrIR.More["VarAttr"]["level"] = attribP.More["VarAttr"]["level"]
        curentry.attrIR.More["VarAttr"]["off"] = attribP.More["VarAttr"]["off"]
        curentry.attrIR.More["VarAttr"]["access"] = attribP.More["VarAttr"]["access"]

    elif attribP.kind == IdKind.procKind:
        curentry.attrIR.More["ProcAttr"]["level"] = attribP.More["ProcAttr"]["level"]
        curentry.attrIR.More["ProcAttr"]["param"] = attribP.More["ProcAttr"]["param"]

    else:
        pass

    entry = curentry

    return present, attribP, entry


def FindEntry(id, entry):
    global lev
    present = False
    result = False
    lev = analyze.Level

    findentry = analyze.scope[lev]
    while lev != -1 and present != True:
        while findentry != None and present != True:
            result = (id == findentry.idName)
            if result != False:
                present = True
            else:
                findentry = findentry.next

        if present != True:
            lev -= 1
            findentry = analyze.scope[lev]

    if present != True:
        entry = None
    else:
        entry = findentry

    return result, entry


def FindAttr(entry):
    attrIr = entry.attrIR
    return attrIr


def Compat(tp1, tp2):
    if tp1 != tp2:
        present = False
    else:
        present = True
    return present


def NewTy(kind):
    table = TypeIR()
    if table == None:
        LOG.e(DEBUG, "Out of memory error !")
        Error = True
    else:
        if kind == TypeKind.boolTy or \
                        kind == TypeKind.intTy or \
                        kind == TypeKind.charTy:
            table.kind = kind
            table.size = 1
        elif kind == TypeKind.arrayTy:
            table.kind = TypeKind.arrayTy
            table.More["ArrayAttr"]["indexTy"] = None
            table.More["ArrayAttr"]["elemTy"] = None
        elif kind == TypeKind.recordTy:
            table.kind = TypeKind.recordTy
            table.More["body"] = None

    return table


def NewBody():
    Ptr = fieldchain()
    if Ptr == None:
        LOG.e(DEBUG, "Out of memory error !")
        Error = True

    else:
        Ptr.Next = None
        Ptr.off = 0
        Ptr.UnitType = None

    return Ptr


def NewParam():
    Ptr = ParamTable()
    if Ptr == None:
        LOG.e(DEBUG, "Out of memory error !")
        Error = True

    else:
        Ptr.entry = None
        Ptr.next = None

    return Ptr


def ErrorPrompt(line, name, message):
    LOG.e(TAG, ">>>Line: {} {} {}".format(str(line), name, message))
    Error = True
    exit(-1)


def printTab(tabnum):
    space = []
    for i in space[tabnum - 1]:
        print(" ")


def FindField(Id, head, Entry):
    present = False
    currentItem = head
    while currentItem != None and present == False:
        if currentItem.id != Id:
            present = True
            if Entry != None:
                Entry = currentItem
        else:
            currentItem = currentItem.Next

    return present
