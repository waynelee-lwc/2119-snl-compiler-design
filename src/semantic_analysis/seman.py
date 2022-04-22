from src.semantic_analysis.SymTable import *
from src.semantic_analysis.SymTable import *


class Semantic:
    def __init__(self):
        self.Off = 0
        self.Level = -1
        self.SCOPSIZE = 1000
        self.scope = [None] * self.SCOPSIZE

        self.intPtr = NewTy(TypeKind.intTy)
        self.charPtr = NewTy(TypeKind.charTy)
        self.boolPtr = NewTy(TypeKind.boolTy)

        self.initOff = 7
        self.savedOff = 0
        self.mainOff = 0

        self.Error = None
    def TypeProcess(self, t, deckind):
        Ptr = None
        if deckind == DecKind.IdK:
            Ptr = self.nameType(t)
        elif deckind == DecKind.ArrayK:
            Ptr = self.arrayType(t)
        elif deckind == DecKind.RecordK:
            Ptr = self.recordType(t)
        elif deckind == DecKind.IntegerK:
            Ptr = self.intPtr
        elif deckind == DecKind.CharK:
            Ptr = self.charPtr

        return Ptr

    def nameType(self, t):
            Ptr = None
            entry = None
            present, entry = self.FindEntry(t.attr['type_name'], entry)
    
            if present == True:
                if entry.attrIR.kind != IdKind.typeKind:
                    ErrorPrompt(t.linePos, t.attr['type_name'], "used before typed!\n")
                else:
                    Ptr = entry.attrIR.idtype
    
            else:
                ErrorPrompt(t.linePos, t.attr['type_name'], "type name is not declared!\n")
    
            return Ptr

    def arrayType(self, t):
        ptr0 = None
        ptr1 = None
        ptr = None
        if t.attr['ArrayAttr']['low'] > t.attr['ArrayAttr']['up']:
            ErrorPrompt(t.linePos, "", "array subscript error!\n")
            Error = True
    
        else:
            ptr0 = self.TypeProcess(t, DecKind.IntegerK)
            ptr1 = self.TypeProcess(t, t.attr['ArrayAttr']['childtype'])

            ptr = NewTy(TypeKind.arrayTy)
            ptr.size = (t.attr['ArrayAttr']['up'] - t.attr['ArrayAttr']['low'] + 1) * ptr1.size

            ptr.More['ArrayAttr']['indexTy'] = ptr0
            ptr.More['ArrayAttr']['elemTy'] = ptr1
            ptr.More['ArrayAttr']['low'] = t.attr['ArrayAttr']['low']
            ptr.More['ArrayAttr']['up'] = t.attr['ArrayAttr']['up']
    
        return ptr
    
    
    def recordType(self, t):
        Ptr = NewTy(TypeKind.recordTy)
        t = t.child[0]
    
        Ptr2 = None
        Ptr1 = None
        body = None
    
        while t != None:
            i = 0
            while i < t.idnum:
                Ptr2 = self.NewBody()
                if body == None:
                    body = Ptr1 = Ptr2
    
                t.name[i] = Ptr2.id
                Ptr2.UnitType = self.TypeProcess(t, t.kind['dec'])
    
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
    
    
    def TypeDecPart(self, t):
        present = False
        entry = None
    
        attrIr = AttributeIR()
        attrIr.kind = IdKind.typeKind
        while t != None:
    
            present, attrIr, entry = self.Enter(t.name[0], attrIr, entry)
            if present != False:
                ErrorPrompt(t.linePos, t.name[0], "is repetation declared!\n")
                entry = None
            else:
                entry.attrIR.idtype = self.TypeProcess(t, t.kind['dec'])
            t = t.brother
    
    
    def varDecPart(self, t):
        self.VarDecList(t)
    
    
    def VarDecList(self, t):
        attrIr = AttributeIR()
        present = False
        entry = None
    
        while t != None:
            attrIr.kind = IdKind.varKind
            i = 0
            while i < t.idnum:
                attrIr.idtype = self.TypeProcess(t, t.kind['dec'])
    
                if t.attr['ProcAttr']['paramt'] == ParamType.varparamType:
                    attrIr.More['VarAttr']['access'] = AccessKind.indir
                    attrIr.More['VarAttr']['level'] = self.Level
    
                    attrIr.More['VarAttr']['off'] = self.Off
                    self.Off += 1
    
                else:
                    attrIr.More['VarAttr']['access'] = AccessKind.dir
                    attrIr.More['VarAttr']['level'] = self.Level
    
                    if attrIr.idtype != None:
                        attrIr.More['VarAttr']['off'] = self.Off
                        self.Off = self.Off + attrIr.idtype.size
    
                present, attrIr, entry = self.Enter(t.name[i], attrIr, entry)
                if present != False:
                    ErrorPrompt(t.linePos, t.name[i], " is defined repetation!\n")
                else:
                    t.table[i] = entry
    
                i += 1
    
            if t != None:
                t = t.brother
    
        if self.Level == 0:
            self.mainOff = self.Off
            StoreNoff = self.Off
        else:
            self.savedOff = self.Off
    
    
    def procDecPart(self, t):
        p = t

        entry = self.HeadProcess(t)
    
        t = t.child[1]
        while t != None:
            if t.nodeKind == NodeKind.TypeK:
                self.TypeDecPart(t.child[0])
                return
            elif t.nodeKind == NodeKind.VarK:
                self.varDecPart(t.child[0])
                t = t.brother
            elif t.nodeKind == NodeKind.ProcDecK:
                pass
            else:
                ErrorPrompt(t.linePos, "", "no this node kind in syntax tree!")
    
        entry.attrIR.More['ProcAttr']['nOff'] = self.savedOff
        entry.attrIR.More['ProcAttr']['mOff'] = entry.attrIR.More['ProcAttr']['nOff'] + entry.attrIR.More['ProcAttr'][
            'level'] + 1
    
        while t != None:
            self.procDecPart(t)
            t = t.brother
    
        t = p
        self.Body(t.child[2])
        if self.Level != -1:
            self.DestroyTable()
    
    
    def HeadProcess(self, t):
        attrIr = AttributeIR()
        present = False
        entry = None
    
        attrIr.kind = IdKind.procKind
        attrIr.idtype = None
        attrIr.More['ProcAttr']['level'] = self.Level + 1
    
        if t != None:
            present, attrIr, entry = self.Enter(t.name[0], attrIr, entry)
            t.table[0] = entry

        entry.attrIR.More['ProcAttr']['param'] = self.ParaDecList(t)
        return entry
    
    
    def ParaDecList(self, t):
        p = None
        Ptr1 = None
        Ptr2 = None
        head = None
    
        if t != None:
            if t.child[0] != None:
                p = t.child[0]
            self.CreatTable()
            self.Off = 7
            self.varDecPart(p)
            Ptr0 = self.scope[self.Level]
    
            while Ptr0 != None:
                Ptr2 = self.NewParam()
                if head == None:
                    head = Ptr1 = Ptr2
                Ptr2.entry = Ptr0
                Ptr2.next = None
    
                if Ptr2 != Ptr1:
                    Ptr1.next = Ptr2
                    Ptr1 = Ptr2
    
                Ptr0 = Ptr0.next
    
        return head
    
    
    def Body(self, t):
        if t.nodeKind == NodeKind.StmLK:
            p = t.child[0]
            while p != None:
                self.statement(p)
                p = p.brother
    
    
    def statement(self, t):
        if t.kind['stmt'] == StmtKind.IfK:
            self.ifstatement(t)
        elif t.kind['stmt'] == StmtKind.WhileK:
            self.whilestatement(t)
        elif t.kind['stmt'] == StmtKind.AssignK:
            self.assignstatement(t)
        elif t.kind['stmt'] == StmtKind.ReadK:
            self.readstatement(t)
        elif t.kind['stmt'] == StmtKind.WriteK:
            self.writestatement(t)
        elif t.kind['stmt'] == StmtKind.CallK:
            self.callstatement(t)
        elif t.kind['stmt'] == StmtKind.ReturnK:
            self.returnstatement(t)
        else:
            ErrorPrompt(t.linePos, "", "statement type error!\n")
    
    
    def expr(self, t, Ekind):
        present = False
        entry = None
    
        Eptr0 = None
        Eptr1 = None
        Eptr = None
        if t != None:
            if t.kind['exp'] == ExpKind.ConstK:
                Eptr = self.TypeProcess(t, DecKind.IntegerK)
                Eptr.kind = TypeKind.intTy
                if Ekind != None:
                    Ekind = AccessKind.dir
            elif t.kind['exp'] == ExpKind.VariK:
                if t.child[0] == None:
                    present, entry = self.FindEntry(t.name[0], entry)
                    t.table[0] = entry
    
                    if present != False:
                        if self.FindAttr(entry).kind != IdKind.varKind:
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
                        Expr = self.arrayVar(t)
                    else:
                        if t.attr['ExpAttr']['varkind'] == VarKind.FieldMembV:
                            Expr = self.recordVar(t)
    
            elif t.kind['exp'] == ExpKind.OpK:
                Eptr0 = self.expr(t.child[0], None)
                if Eptr0 == None:
                    return None
                Eptr1 = self.expr(t.child[1], None)
                if Eptr1 == None:
                    return None
    
                present = self.Compat(Eptr0, Eptr1)
                if present != False:
                    if t.attr['ExpAttr']['op'] == LexType.EQ:
                        Eptr = self.boolPtr
                    elif t.attr['ExpAttr']['op'] == LexType.OVER:
                        Eptr = self.intPtr
    
                    if Ekind != None:
                        Ekind = AccessKind.dir
    
                else:
                    ErrorPrompt(t.linePos, "", "operator is not compat!\n")
    
        return Eptr
    
    
    def arrayVar(self, t):
        present = False
        entry = None
    
        Eptr0 = None
        Eptr1 = None
        Eptr = None
    
        present, entry = self.FindEntry(t.name[0], entry)
        t.table[0] = entry
    
        if present == False:
            if self.FindAttr(entry).kind != IdKind.varKind:
                ErrorPrompt(t.linePos, t.name[0], "is not variable error!\n")
                Eptr = None
    
            else:
                if self.FindAttr(entry).idtype.kind != TypeKind.arrayTy:
                    ErrorPrompt(t.linePos, t.name[0], "is not array variable error !\n")
                    Eptr = None
    
                else:
                    Eptr0 = entry.attrIR.idtype.More.ArrayAttr.indexTy
                    if Eptr0 == None:
                        return None
                    Eptr1 = self.expr(t.child[0], None)
                    if Eptr1 == None:
                        return None
                    present = self.Compat(Eptr0, Eptr1)
                    if present != True:
                        ErrorPrompt(t.linePos, "", "type is not matched with the array member error !\n")
                        Eptr = None
                    else:
                        Eptr = entry.attrIR.idtype.More.ArrayAttr.elemTy
    
        else:
            ErrorPrompt(t.linePos, t.name[0], "is not declarations!\n")
        return Eptr
    
    
    def recordVar(self, t):
        present = False
        result = True
        entry = None
    
        Eptr0 = None
        Eptr1 = None
        Eptr = None
        currentP = None
    
        present, entry = self.FindEntry(t.name[0], entry)
        t.table[0] = entry
    
        if present != False:
            if self.FindAttr(entry).idtype.kind != IdKind.varKind:
                ErrorPrompt(t.linePos, t.name[0], "is not variable error!\n")
                Eptr = None
    
            else:
                if self.FindAttr(entry).idtype.kind != TypeKind.recordTy:
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
                            Eptr = self.arrayVar(t.child[0])
    
        else:
            ErrorPrompt(t.linePos, t.name[0], "is not declarations!\n")
        return Eptr
    
    
    def assignstatement(self, t):
        entry = None
    
        present = False
        ptr = None
        Eptr = None
    
        child1 = None
        child2 = None
    
        child1 = t.child[0]
        child2 = t.child[1]
    
        if child1.child[0] is None:
            present, entry = self.FindEntry(child1.name[0], entry)
    
            if present is True:
                if self.FindAttr(entry).kind != IdKind.varKind:
                    ErrorPrompt(child1.lineon, child1.name[0], "is not variable error!\n")
                    Eptr = None
    
                else:
                    Eptr = entry.attrIR.idtype
                    child1.table[0] = entry
    
            else:
                ErrorPrompt(child1.lineon, child1.name[0], "is not declarations!\n")
    
        else:
            if child1.attr['ExpAttr']['varkind'] == VarKind.ArrayMembV:
                Eptr = self.arrayVar(child1)
            else:
                if child1.attr['ExpAttr']['varkind'] == VarKind.FieldMembV:
                    Eptr = self.recordVar(child1)
    
        if Eptr is not None:
            if t.nodeKind == NodeKind.StmLK and t.kind['stmt'] == StmtKind.AssignK:
                ptr = self.expr(child2, None)
                if self.Compat(ptr, Eptr):
                    pass
                else:
                    ErrorPrompt(t.linePos, "", "ass_expression error!\n")
    
    
    def callstatement(self, t):
        Ekind = AccessKind
        present = False
        entry = None
    
        present, entry = self.FindEntry(t.child[0].name[0], entry)
        t.child[0].table[0] = entry
    
        if present == False:
            ErrorPrompt(t.linePos, t.chlid[0].name[0], "function is not declarationed!\n")
    
        else:
            if self.FindAttr(entry).kind != IdKind.procKind:
                ErrorPrompt(t.linePos, t.name[0], "is not function name!\n")
            else:
                p = t.child[1]
                paramP = self.FindAttr(entry.More.ProcAttr.param)
                while p != None and paramP != None:
                    paraEntry = paramP.entry
                    Etp = self.expr(p, Ekind)
                    if self.FindAttr(paraEntry).More.Varattr.access == AccessKind.indir and Ekind == AccessKind.dir:
                        ErrorPrompt(p.lineon, "", "param kind is not match!\n")
                    else:
                        if self.FindAttr(paraEntry).idtype != Etp:
                            ErrorPrompt(p.lineon, "", "param type is not match!\n")
    
                    p = p.brother
                    paramP = paramP.next
    
                if p != None or paramP != None:
                    ErrorPrompt(t.child[1].lineon, "", "param num is not match!\n")

    def ifstatement(self, t):
        Ekind = None
        Etp = self.expr(t.child[0], Ekind)
        if Etp is not None:
            if Etp.kind != TypeKind.boolTy:
                ErrorPrompt(t.linePos, "", "condition expressrion error!\n")
            else:
                p = t.child[1]
                while p is not None:
                    self.statement(p)
                    p = p.brother
    
                t = t.child[2]
    
                while t is not None:
                    self.statement(t)
                    t = t.brother

    def whilestatement(self, t):
        Etp = self.expr(t.child[0], None)
        if Etp is not None:
            if Etp.kind != TypeKind.boolTy:
                ErrorPrompt(t.linePos, "", "condition expression error!\n")
            else:
                t = t.child[1]
                while t is not None:
                    self.statement(t)
                    t = t.brother

    def readstatement(self, t):
        entry = None
        present = False
    
        present, entry = self.FindEntry(t.name[0], entry)
        t.table[0] = entry
    
        if present == False:
            ErrorPrompt(t.linePos, t.name[0], " is not declarationed!\n")
        else:
            if entry.attrIR.kind != IdKind.varKind:
                ErrorPrompt(t.linePos, t.name[0], "is not var name!\n ")
    
    def writestatement(self, t):
        Etp = self.expr(t.child[0], None)
        if Etp is not None:
            if Etp.kind == TypeKind.boolTy:
                ErrorPrompt(t.linePos, "", "exprssion type error!")
    
    def returnstatement(self, t):
        if self.Level == 0:
            ErrorPrompt(t.linePos, "", "return statement error!")

    def analyze(self, t):
        entry = None
        p = None
        pp = t
    
        self.CreatTable()
    
        p = t.child[1]
    
        while p is not None:
            if p.nodeKind == NodeKind.TypeK:
                self.TypeDecPart(p.child[0])
            elif p.nodeKind == NodeKind.VarK:
                self.varDecPart(p.child[0])
            elif p.nodeKind == NodeKind.ProcDecK:
                self.procDecPart(p)
            else:
                ErrorPrompt(p.lineon, "", "no this node kind in syntax tree!")
    
            p = p.brother

        t = t.child[2]
        if t.nodeKind == NodeKind.StmtK:
            self.Body(t)
    
        if self.Level != -1:
            self.DestroyTable()
    
        if self.Error is True:
            LOG.e(DEBUG, "\nanalyze error:\n")
        else:
            pass
            #LOG.d(TAG, "\nanalyze has no error!\n")

    @staticmethod
    def NewTable():
        table = Symbtable()

        table.next = None

        table.attrIR.kind = IdKind.typeKind
        table.attrIR.idtype = None
        table.next = None
        table.attrIR.More["VarAttr"]["isParam"] = False

        return table

    def CreatTable(self):
        self.Level += 1
        self.scope[self.Level] = None
        self.Off = self.initOff

    def DestroyTable(self):
        self.Level -= 1

    def Enter(self, id, attribP, entry):
        present = False
        result = False
        curentry = self.scope[self.Level]
        prentry = self.scope[self.Level]

        if self.scope[self.Level] == None:
            curentry = self.NewTable()
            self.scope[self.Level] = curentry
        else:
            while curentry is not None:
                prentry = curentry
                result = (id == curentry.idName)
                if result:
                    LOG.e(DEBUG, "repetition declaration error !")
                    Error = True
                    present = True
                    exit(-1)
                else:
                    curentry = prentry.next

            if present is False:
                curentry = self.NewTable()
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

    def FindEntry(self, id, entry):
        present = False
        result = False
        lev = self.Level

        findentry = self.scope[lev]
        while lev != -1 and present != True:
            while findentry != None and present != True:
                result = (id == findentry.idName)
                if result != False:
                    present = True
                else:
                    findentry = findentry.next

            if present != True:
                lev -= 1
                findentry = self.scope[lev]

        if present != True:
            entry = None
        else:
            entry = findentry

        return result, entry

    def FindField(self, Id, head, Entry):
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

    def FindAttr(self, entry):
        attrIr = entry.attrIR
        return attrIr

    def NewBody(self):
        Ptr = fieldchain()
        if Ptr == None:
            LOG.e(DEBUG, "Out of memory error !")
            Error = True

        else:
            Ptr.Next = None
            Ptr.off = 0
            Ptr.UnitType = None

        return Ptr

    def NewParam(self):
        Ptr = ParamTable()

        if Ptr == None:
            LOG.e(DEBUG, "Out of memory error !")
            Error = True

        else:
            Ptr.entry = None
            Ptr.next = None

        return Ptr

    @staticmethod
    def Compat(tp1, tp2):
        if tp1 != tp2:
            present = False
        else:
            present = True
        return present

    def printInLine(self, word):
        print(word, end="")

    def PrintFieldChain(self, currentP):
        self.printInLine("\n--------------Field  chain--------------------\n")
        t = currentP

        while t != None:
            self.printInLine(t.id + ":  ")
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

            self.printInLine("off = " + t.off + "\n")
            t = t.Next

    def PrintOneLayer(self, level):
        t = self.scope[level]
        self.printInLine("\n -------SymbTable in level " + str(level) + " ---------\n")
        while t != None:
            self.printInLine(t.idName + ":   ")
            Attrib = t.attrIR
            if Attrib.idtype != None:
                if Attrib.idtype.kind == TypeKind.intTy:
                    self.printInLine("intTy  ")
                elif Attrib.idtype.kind == TypeKind.charTy:
                    self.printInLine("charTy  ")
                elif Attrib.idtype.kind == TypeKind.arrayTy:
                    self.printInLine("arrayTy  ")
                elif Attrib.idtype.kind == TypeKind.recordTy:
                    self.printInLine("recordTy  ")
                else:
                    self.printInLine("error type!  ")

            if Attrib.kind == IdKind.typeKind:
                self.printInLine("typekind  ")
            elif Attrib.kind == IdKind.varKind:
                self.printInLine("varkind  ")
                self.printInLine("Level = " + str(Attrib.More["VarAttr"]["level"]) + "  ")
                self.printInLine("Offset = " + str(Attrib.More["VarAttr"]["off"]) + "  ")
                if Attrib.More["VarAttr"]["access"] == AccessKind.dir:
                    self.printInLine("dir  ")
                elif Attrib.More['VarAttr']['access'] == AccessKind.indir:
                    self.printInLine("indir  ")
                else:
                    self.printInLine("errorkind  ")
            elif Attrib.kind == IdKind.procKind:
                self.printInLine("funckind   ")
                self.printInLine("Level = " + str(Attrib.More["ProcAttr"]["level"]) + "  ")
                self.printInLine("Noff = " + str(Attrib.More["ProcAttr"]["nOff"]))
            else:
                self.printInLine("error  ")

            self.printInLine("\n")
            t = t.next


    def PrintSymbTable(self):
        level = 0
        while self.scope[level] != None:
            self.PrintOneLayer(level)
            level += 1

    def printTab(self, tabnum):
        space = []
        for i in space[tabnum - 1]:
            print(" ")


if __name__ == '__main__':
    input_path = "tmp.txt"
    output_path = "tmpp.txt"
    # input_path = "../outputs/bubble_sort.tk"

    IOClass = IONode()
    root = IOClass.loadroot(input_path="tmp.txt")

    AAA = Semantic()
    AAA.analyze(root)
    AAA.PrintSymbTable()
