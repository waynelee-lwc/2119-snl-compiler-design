from src.semantic_analysis.SemanticSupport import *


class Semantic:
    def __init__(self):
        self.Off = 0
        self.Level = -1
        self.beginLevel = 0
        self.SCOPSIZE = 1000
        self.scope = [None] * self.SCOPSIZE

        self.intPtr = NewTy(TypeKind.intTy)
        self.charPtr = NewTy(TypeKind.charTy)
        self.boolPtr = NewTy(TypeKind.boolTy)

        self.initOff = 7
        self.savedOff = 0
        self.mainOff = 0

        self.error = []

        self.out = []

    def TypeProcess(self, t, deckind):
        if deckind == DecKind.IdK:
            return self.nameType(t)
        elif deckind == DecKind.ArrayK:
            return self.arrayType(t)
        elif deckind == DecKind.RecordK:
            return self.recordType(t)
        elif deckind == DecKind.IntegerK:
            return self.intPtr
        elif deckind == DecKind.CharK:
            return self.charPtr

    def nameType(self, t):
        Ptr = None
        present, entry = self.FindEntry(t.attr['type_name'])

        if present is True:
            if entry.attrIR.kind != IdKind.typeKind:
                self.error.append("in line:{0},col{1}, {2} used before typed\n".format(t.linePos, t.colPos, t.attr['type_name']))
                #ErrorPrompt(t.linePos, t.attr['type_name'], "used before typed!\n")
            else:
                Ptr = entry.attrIR.idtype
        else:
            self.error.append(
                "in line:{0},col{1}, {2} is not declared\n".format(t.linePos, t.colPos, t.attr['type_name']))
            # ErrorPrompt(t.linePos, t.attr['type_name'], "type name is not declared!\n")

        return Ptr

    def arrayType(self, t):
        ptr = None
        if t.attr['ArrayAttr']['low'] > t.attr['ArrayAttr']['up']:
            self.error.append(
                "in line:{0},col{1}, array {2} has wrong index\n".format(t.linePos, t.colPos,t.name[0]))
            # ErrorPrompt(t.linePos, "", "array subscript error!\n")

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

        while t is not None:
            for i in range(0, t.idnum):
                Ptr2 = self.NewBody()
                if body is None:
                    Ptr1 = Ptr2
                    body = Ptr2

                Ptr2.id = t.name[i]
                Ptr2.UnitType = self.TypeProcess(t, t.kind['dec'])

                Ptr2.Next = None

                if Ptr2 != Ptr1:
                    Ptr2.off = Ptr1.off + Ptr1.UnitType.size
                    Ptr1.Next = Ptr2
                    Ptr1 = Ptr2

            t = t.brother
        Ptr.size = Ptr2.off + Ptr2.UnitType.size
        Ptr.More['body'] = body
        return Ptr

    def TypeDecPart(self, t):
        attr = AttributeIR()
        attr.kind = IdKind.typeKind
        while t is not None:
            present, attr, entry = self.Enter(t.name[0], attr, t.linePos, t.colPos)
            if present is True:
                self.error.append("in line:{0} col:{1}, {2}is repetation declared!\n".format(t.linePos, t.colPos, t.name[0]))
                # ErrorPrompt(t.linePos, t.name[0], "is repetation declared!\n")
            else:
                entry.attrIR.idtype = self.TypeProcess(t, t.kind['dec'])
            t = t.brother

    def varDecPart(self, t):
        self.VarDecList(t)

    def VarDecList(self, t):
        attr = AttributeIR()

        while t is not None:
            attr.kind = IdKind.varKind
            for i in range(0, t.idnum):
                attr.idtype = self.TypeProcess(t, t.kind['dec'])

                if t.attr['ProcAttr']['paramt'] == ParamType.varparamType:
                    attr.More['VarAttr']['access'] = AccessKind.indir
                    attr.More['VarAttr']['level'] = self.Level
                    attr.More['VarAttr']['off'] = self.Off
                    self.Off += 1
                else:
                    attr.More['VarAttr']['access'] = AccessKind.dir
                    attr.More['VarAttr']['level'] = self.Level
                    if attr.idtype is not None:
                        attr.More['VarAttr']['off'] = self.Off
                        self.Off = self.Off + attr.idtype.size

                present, attr, entry = self.Enter(t.name[i], attr, t.linePos, t.colPos)
                if present is True:
                    self.error.append(
                        "in line:{0} col:{1}, {2}is repetition defined\n".format(t.linePos, t.colPos, t.name[i]))
                    # ErrorPrompt(t.linePos, t.name[i], " is defined repetation!\n")
                else:
                    t.table[i] = entry

            if t is not None:
                t = t.brother

        if self.Level == 0:
            self.mainOff = self.Off
        else:
            self.savedOff = self.Off

    def procDecPart(self, t):
        self.CreatTable()
        self.Off = 7
        p = t
        entry = self.HeadProcess(t)

        t = t.child[1]
        while t is not None:
            if t.nodeKind == NodeKind.TypeK:
                self.TypeDecPart(t.child[0])
                t = t.brother
            elif t.nodeKind == NodeKind.VarK:
                self.varDecPart(t.child[0])
                t = t.brother
            elif t.nodeKind == NodeKind.ProcDecK:
                break
            else:
                self.error.append(
                    "in line:{0}, no this part in procedure declaration part\n".format(t.linePos))
                # ErrorPrompt(t.linePos, "", "no this node kind in syntax tree!")
        entry.attrIR.More['ProcAttr']['nOff'] = self.savedOff
        entry.attrIR.More['ProcAttr']['mOff'] = entry.attrIR.More['ProcAttr']['nOff'] + entry.attrIR.More['ProcAttr'][
            'level'] + 1
        while t is not None:
            self.procDecPart(t)
            t = t.brother

        t = p

        self.Body(t.child[2])
        if self.Level != -1:
            self.DestroyTable()

    def HeadProcess(self, t):
        attrIr = AttributeIR()
        entry = None

        attrIr.kind = IdKind.procKind
        attrIr.idtype = None
        attrIr.More['ProcAttr']['level'] = self.Level

        if t is not None:
            present, attrIr, entry = self.Enter(t.name[0], attrIr, t.linePos, t.colPos)
            t.table[0] = entry

        entry.attrIR.More['ProcAttr']['param'] = self.ParaDecList(t)
        return entry

    def ParaDecList(self, t):
        p = None
        Ptr1 = None
        Ptr2 = None
        head = None

        if t is not None:
            if t.child[0] is not None:
                p = t.child[0]
            self.varDecPart(p)
            Ptr0 = self.scope[self.Level]

            while Ptr0 is not None:
                Ptr2 = self.NewParam()
                if head is None:
                    Ptr1 = Ptr2
                    head = Ptr2
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
            while p is not None:
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
            self.error.append(
                "in line:{0} col:{1}, {2} statement type error\n".format(t.linePos, t.colPos, t.name[0]))

            #ErrorPrompt(t.linePos, "", "statement type error!\n")

    def expr(self, t, Ekind):
        present = False
        entry = None

        Eptr0 = None
        Eptr1 = None
        Eptr = None
        if t is not None:
            if t.kind['exp'] == ExpKind.ConstK:
                Eptr = self.TypeProcess(t, DecKind.IntegerK)
                Eptr.kind = TypeKind.intTy
                if Ekind is not None:
                    Ekind = AccessKind.dir
            elif t.kind['exp'] == ExpKind.VariK:
                if t.child[0] is not None:
                    present, entry = self.FindEntry(t.name[0])
                    t.table[0] = entry

                    if present is True:
                        if self.FindAttr(entry).kind != IdKind.varKind:
                            self.error.append(
                                "in line:{0} col:{1}, {2} is not variable\n".format(t.linePos, t.colPos,
                                                                                         t.name[0]))
                            # ErrorPrompt(t.linePos, t.name[0], "is not variable error!\n")
                            Eptr = None
                        else:
                            Eptr = entry.attrIR.idtype
                            if Ekind is not None:
                                Ekind = AccessKind.indir

                    else:
                        self.error.append(
                            "in line:{0} col:{1}, {2}is not declares\n".format(t.linePos, t.colPos,
                                                                                     t.name[0]))

                        #ErrorPrompt(t.linePos, t.name[0], "is not declarations!\n")

                else:
                    if t.attr['ExpAttr']['varkind'] == VarKind.ArrayMembV:
                        Eptr = self.arrayVar(t)
                    elif t.attr['ExpAttr']['varkind'] == VarKind.FieldMembV:
                        Eptr = self.recordVar(t)

            elif t.kind['exp'] == ExpKind.OpK:
                Eptr0 = self.expr(t.child[0], None)
                if Eptr0 is None:
                    return None
                Eptr1 = self.expr(t.child[1], None)
                if Eptr1 is None:
                    return None

                present = self.Compat(Eptr0, Eptr1)
                if present is True:
                    if t.attr['ExpAttr']['op'] == LexType.EQ:
                        Eptr = self.boolPtr
                    elif t.attr['ExpAttr']['op'] == LexType.OVER:
                        Eptr = self.intPtr

                    if Ekind is not None:
                        Ekind = AccessKind.dir

                else:
                    self.error.append(
                        "in line:{0} col:{1}, {2} operator is not compat\n".format(t.linePos, t.colPos,
                                                                                 t.name[0]))

                    # ErrorPrompt(t.linePos, "", "operator is not compat!\n")

        return Eptr

    def arrayVar(self, t):
        Eptr0 = None
        Eptr1 = None
        Eptr = None

        present, entry = self.FindEntry(t.name[0])
        t.table[0] = entry

        if present is False:
            if self.FindAttr(entry).kind != IdKind.varKind:
                self.error.append(
                    "in line:{0} col:{1}, {2} is not variable\n".format(t.linePos, t.colPos,
                                                                             t.name[0]))

                # ErrorPrompt(t.linePos, t.name[0], "is not variable error!\n")
                Eptr = None

            else:
                if self.FindAttr(entry).idtype.kind != TypeKind.arrayTy:
                    self.error.append(
                    "in line:{0} col:{1}, {2} is not array variable\n".format(t.linePos, t.colPos,
                                                                             t.name[0]))

                    # ErrorPrompt(t.linePos, t.name[0], "is not array variable error !\n")
                    Eptr = None

                else:
                    Eptr0 = entry.attrIR.idtype.More.ArrayAttr.indexTy
                    if Eptr0 is None:
                        return None
                    Eptr1 = self.expr(t.child[0], None)
                    if Eptr1 is None:
                        return None
                    present = self.Compat(Eptr0, Eptr1)
                    if present is False:
                        self.error.append(
                            "in line:{0} col:{1}, {2} type cannot match the array member\n".format(t.linePos, t.colPos,
                                                                                      t.name[0]))
                        # ErrorPrompt(t.linePos, "", "type is not matched with the array member error !\n")
                        Eptr = None
                    else:
                        Eptr = entry.attrIR.idtype.More.ArrayAttr.elemTy

        else:
            self.error.append(
                "in line:{0} col:{1}, {2} is not declared\n".format(t.linePos, t.colPos,
                                                                          t.name[0]))
            # ErrorPrompt(t.linePos, t.name[0], "is not declarations!\n")
        return Eptr

    def recordVar(self, t):
        result = True

        Eptr0 = None
        Eptr1 = None
        Eptr = None
        cur = None

        present, entry = self.FindEntry(t.name[0])
        t.table[0] = entry

        if present is True:
            if self.FindAttr(entry).idtype.kind != IdKind.varKind:
                self.error.append(
                    "in line:{0} col:{1}, {2} is not variable\n".format(t.linePos, t.colPos,
                                                                              t.name[0]))
                # ErrorPrompt(t.linePos, t.name[0], "is not variable error!\n")
                Eptr = None

            else:
                if self.FindAttr(entry).idtype.kind != TypeKind.recordTy:
                    self.error.append(
                        "in line:{0} col:{1}, {2} is not record variable\n".format(t.linePos, t.colPos, t.name[0]))

                    # ErrorPrompt(t.linePos, t.name[0], "is not record variable error !\n")
                    Eptr = None

                else:
                    Eptr0 = entry.attrIR.idtype
                    cur = Eptr0.More.body
                    while cur is not None and result is True:
                        result = (t.child[0].name[0] == cur.id)
                        if result is False:
                            Eptr = cur.UnitType
                        else:
                            cur = cur.Next

                    if cur is not None:
                        if result is True:
                            self.error.append(
                                "in line:{0} col:{1}, {2} is not field type\n".format(t.linePos, t.colPos,
                                                                                    t.name[0]))

                            # ErrorPrompt(t.child[0].linePos, t.child[0].name[0], "is not field type!\n")
                            Eptr = self.arrayVar(t.child[0])

        else:
            self.error.append(
                "in line:{0} col:{1}, {2} is not declared\n".format(t.linePos, t.colPos,
                                                                    t.name[0]))

            # ErrorPrompt(t.linePos, t.name[0], "is not declarations!\n")
        return Eptr

    def assignstatement(self, t):
        Eptr = None

        child1 = t.child[0]
        child2 = t.child[1]

        if child1.child[0] is None:
            present, entry = self.FindEntry(child1.name[0])

            if present is True:
                if self.FindAttr(entry).kind != IdKind.varKind:
                    self.error.append(
                        "in line:{0} col:{1}, {2} is not variable\n".format(child1.linePos, child1.colPos, child1.name[0]))

                    # ErrorPrompt(child1.lineon, child1.name[0], "is not variable error!\n")
                    Eptr = None
                else:
                    Eptr = entry.attrIR.idtype
                    child1.table[0] = entry
            else:
                self.error.append(
                    "in line:{0} col:{1}, {2} is not declared\n".format(child1.linePos, child1.colPos, child1.name[0]))
                #ErrorPrompt(child1.lineon, child1.name[0], "is not declarations!\n")

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
                    self.error.append(
                        "in line:{0} assignment wrong\n".format(t.linePos))

                    # ErrorPrompt(t.linePos, "", "ass_expression error!\n")

    def callstatement(self, t):
        Ekind = AccessKind

        present, entry = self.FindEntry(t.child[0].name[0])
        t.child[0].table[0] = entry

        if present is False:
            self.error.append(
                "in line:{0} col:{1}, {2} function is not declared\n".format(t.linePos, t.colPos, t.child[0].name[0]))

            #ErrorPrompt(t.linePos, t.chlid[0].name[0], "function is not declarationed!\n")

        else:
            if self.FindAttr(entry).kind != IdKind.procKind:
                self.error.append(
                    "in line:{0} col:{1}, {2} is not function name\n".format(t.linePos, t.colPos, t.name[0]))
                #ErrorPrompt(t.linePos, t.name[0], "is not function name!\n")
            else:
                p = t.child[1]
                Param = self.FindAttr(entry.More.ProcAttr.param)
                while p is not None and Param is not None:
                    paramEntry = Param.entry
                    Etp = self.expr(p, Ekind)
                    if self.FindAttr(paramEntry).More.Varattr.access == AccessKind.indir and Ekind == AccessKind.dir:
                        self.error.append(
                            "in line:{0} col:{1}, {2} kind match wrong\n".format(p.linePos, p.colPos, p.name[0]))
                        # ErrorPrompt(p.lineon, "", "param kind is not match!\n")
                    elif self.FindAttr(paramEntry).idtype != Etp:
                        self.error.append(
                            "in line:{0} col:{1}, {2} type match wrong\n".format(p.linePos, p.colPos, p.name[0]))

                        # ErrorPrompt(p.lineon, "", "param type is not match!\n")

                    p = p.brother
                    Param = Param.next

                if p is not None or Param is not None:
                    self.error.append(
                        "in line:{0}, wrong in matching parameters because of num\n".format(t.child[1].linePos))

                    #ErrorPrompt(t.child[1].lineon, "", "param num is not match!\n")

    def ifstatement(self, t):
        Etp = self.expr(t.child[0], None)
        if Etp is not None:
            if Etp.kind != TypeKind.boolTy:
                self.error.append(
                    "in line:{0}, condition is not a bool expression\n".format(t.linePos))

                # ErrorPrompt(t.linePos, "", "condition expressrion error!\n")
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
                self.error.append(
                    "in line:{0}, while condition error\n".format(t.linePos))

                # ErrorPrompt(t.linePos, "", "condition expression error!\n")
            else:
                t = t.child[1]
                while t is not None:
                    self.statement(t)
                    t = t.brother

    def readstatement(self, t):
        present, entry = self.FindEntry(t.name[0])
        t.table[0] = entry

        if present is False:
            self.error.append(
                "in line:{0} col:{1}, {2} is not declared\n".format(t.linePos, t.colPos, t.name[0]))

            # ErrorPrompt(t.linePos, t.name[0], " is not declarationed!\n")
        else:
            if entry.attrIR.kind != IdKind.varKind:
                self.error.append(
                    "in line:{0} col:{1}, {2} is not variable\n".format(t.linePos, t.colPos, t.name[0]))

                # ErrorPrompt(t.linePos, t.name[0], "is not var name!\n ")

    def writestatement(self, t):
        Etp = self.expr(t.child[0], None)
        if Etp is not None:
            if Etp.kind == TypeKind.boolTy:
                self.error.append("in line:{0}, \n".format(t.linePost))
                self.error.append(
                    "in line:{0}, cannot write bool expression\n".format(t.linePos))
                # ErrorPrompt(t.linePos, "", "write error!")

    def returnstatement(self, t):
        if self.Level == 0:
            self.error.append(
                "in line:{0}, wrong return statement\n".format(t.linePos))

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
                self.error.append(
                    "in line:{0} col:{1}, {2} no this in syntax tree\n".format(p.linePos, t.colPos, t.name[0]))

                # ErrorPrompt(p.linePos, "", "no this node kind in syntax tree!")

            p = p.brother

        t = t.child[2]
        if t.nodeKind == NodeKind.StmtK:
            self.Body(t)

        if self.Level != -1:
            self.DestroyTable()

        if len(self.error) != 0:
            print(self.error)
            # LOG.e(DEBUG, "\nanalyze error:\n")
        else:
            pass
            # LOG.d(TAG, "\nanalyze has no error!\n")
    @staticmethod
    def GetTableItem():
        table = SymTableItem()

        table.attrIR.kind = IdKind.typeKind
        table.attrIR.More["VarAttr"]["isParam"] = False

        return table

    def CreatTable(self):
        self.Level += 1
        self.scope[self.Level] = None
        self.Off = self.initOff

    def DestroyTable(self):
        self.PrintOneLayer(self.Level)
        self.scope[self.Level] = None
        self.Level -= 1
        # self.PrintOneLayer(self.Level)

    def Enter(self, id, attribP, line, col):
        present = False
        cur = self.scope[self.Level]
        pre = self.scope[self.Level]

        if self.scope[self.Level] is None:
            cur = self.GetTableItem()
            self.scope[self.Level] = cur
        else:
            while cur is not None:
                pre = cur
                # result = (id == cur.idName)
                if id == cur.idName:
                    self.error.append("\(line:{0} col:{1}\),word {2}, repetition declaration error !".format(line, col, id))
                    # LOG.e(DEBUG, "repetition declaration error !")
                    present = True
                    return present, cur.attrIR, cur
                else:
                    cur = pre.next

            if present is False:
                cur = self.GetTableItem()
                pre.next = cur

        cur.idName = id
        cur.attrIR.idtype = attribP.idtype

        cur.attrIR.kind = attribP.kind
        if attribP.kind == IdKind.typeKind:
            pass
        elif attribP.kind == IdKind.varKind:
            cur.attrIR.More["VarAttr"]["level"] = attribP.More["VarAttr"]["level"]
            cur.attrIR.More["VarAttr"]["off"] = attribP.More["VarAttr"]["off"]
            cur.attrIR.More["VarAttr"]["access"] = attribP.More["VarAttr"]["access"]

        elif attribP.kind == IdKind.procKind:
            cur.attrIR.More["ProcAttr"]["level"] = attribP.More["ProcAttr"]["level"]
            cur.attrIR.More["ProcAttr"]["param"] = attribP.More["ProcAttr"]["param"]

        return present, attribP, cur

    def FindEntry(self, id):
        r1 = False
        present = False
        level = self.Level

        entry = self.scope[level]
        while level != -1 and r1 is False:
            while entry is not None and r1 is not True:
                present = (id == entry.idName)
                if present is True:
                    r1 = True
                else:
                    entry = entry.next

            if r1 is False:
                level -= 1
                entry = self.scope[level]

        if r1 is False:
            entry = None

        return present, entry

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
        Ptr.off = 0
        return Ptr

    def NewParam(self):
        Ptr = ParamTable()

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

    def printWord(self, word):
        print(word, end="")

    @staticmethod
    def getOneJson(level_flag='', name='', type_='', kind='', level='', offset='', dir=''):
        tmp = {'level_flag': level_flag, 'name': name, 'type': type_, 'kind': kind, 'level': level, 'offset': offset,
               'dir': dir, 'noff': ''}
        return tmp

    def PrintOneLayer(self, level):
        t = self.scope[level]
        self.printWord("\n -------SymbTable in level " + str(level) + " ---------\n")
        self.out.append(self.getOneJson(level_flag=str(level)))
        while t is not None:
            tmp_json = self.getOneJson()
            self.printWord(t.idName + ":   ")
            tmp_json["name"] = t.idName
            Attrib = t.attrIR
            if Attrib.idtype is not None:
                if Attrib.idtype.kind == TypeKind.intTy:
                    self.printWord("intTy  ")
                    tmp_json["type_"] = "intTy"
                elif Attrib.idtype.kind == TypeKind.charTy:
                    self.printWord("charTy  ")
                    tmp_json["type_"] = "charTy"
                elif Attrib.idtype.kind == TypeKind.arrayTy:
                    self.printWord("arrayTy  ")
                    tmp_json["type_"] = "arrayTy"
                elif Attrib.idtype.kind == TypeKind.recordTy:
                    self.printWord("recordTy  ")
                    tmp_json["type_"] = "recordTy"
                else:
                    self.printWord("error type!  ")
            if Attrib.kind == IdKind.typeKind:
                self.printWord("typekind  ")
                tmp_json["kind"] = "typekind"
            elif Attrib.kind == IdKind.varKind:
                self.printWord("varkind  ")
                self.printWord("Level = " + str(Attrib.More["VarAttr"]["level"]) + "  ")
                self.printWord("Offset = " + str(Attrib.More["VarAttr"]["off"]) + "  ")
                tmp_json["kind"] = "varkind"
                tmp_json["level"] = str(Attrib.More["VarAttr"]["level"])
                tmp_json["offset"] = str(Attrib.More["VarAttr"]["off"])
                if Attrib.More["VarAttr"]["access"] == AccessKind.dir:
                    self.printWord("dir  ")
                    tmp_json["dir"] = "dir"
                elif Attrib.More['VarAttr']['access'] == AccessKind.indir:
                    self.printWord("indir  ")
                    tmp_json["dir"] = "indir"
                else:
                    self.printWord("errorkind  ")
            elif Attrib.kind == IdKind.procKind:
                self.printWord("funckind   ")
                self.printWord("Level = " + str(Attrib.More["ProcAttr"]["level"]) + "  ")
                self.printWord("Noff = " + str(Attrib.More["ProcAttr"]["nOff"]))
                tmp_json["kind"] = "funckind"
                tmp_json["level"] = str(Attrib.More["VarAttr"]["level"])
                tmp_json["noff"] = str(Attrib.More["ProcAttr"]["nOff"])
            else:
                self.printWord("error  ")

            self.printWord("\n")
            t = t.next
            self.out.append(tmp_json)

    def PrintSymbTable(self):
        level = 0
        while self.scope[level] != None:
            self.PrintOneLayer(level)
            level += 1

    def GetResult(self):
        return self.out, self.error


if __name__ == '__main__':

    programPath = sys.argv[1]   #程序产物文件夹
    input_path = programPath + '/treell1'
    output_path = programPath + '/sem'
    error_path = programPath + '/semerr'

    # input_path = "tmp1.txt"
    # output_path = None
    # error_path = None
    # output_path = "tmpp.txt"
    # input_path = "../outputs/bubble_sort.tk"

    IOClass = IONode()
    root = IOClass.loadroot(input_path=input_path)

    AAA = Semantic()
    AAA.analyze(root)

    table, error = AAA.GetResult()

    print(table)
    print(error)

    # with open(output_path, 'w') as f:
    #     print(table, file=f)
    # if len(error) != 0:
    #     with open(error_path, 'w') as f:
    #         print(error, file=f)

    # AAA.PrintSymbTable()
    # js1 = open("js1", 'w')
    # print(AAA.out, file=js1)
    # js1.close()
