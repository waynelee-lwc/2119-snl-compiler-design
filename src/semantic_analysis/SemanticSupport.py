import sys
from enum import Enum


class LexType(Enum):
    ENDFILE = 1
    ERROR = 2
    PROGRAM = 3
    PROCEDURE = 4
    TYPE = 5
    VAR = 6
    IF = 7
    THEN = 8
    ELSE = 9
    FI = 10
    WHILE = 11
    DO = 12
    ENDWH = 13
    BEGIN = 14
    END = 15
    READ = 16
    WRITE = 17
    ARRAY = 18
    OF = 19
    RECORD = 20
    RETURN = 21
    INTEGER = 22
    CHAR = 23
    ID = 24
    INTC = 25
    ASSIGN = 26
    CHARC = 27
    LT = 28
    EQ = 29
    PLUS = 30
    MINUS = 31
    TIMES = 32
    OVER = 33
    LPAREN = 34
    RPAREN = 35
    DOT = 36
    COLON = 37
    SEMI = 38
    COMMA = 39
    LMIDPAREN = 40
    RMIDPAREN = 41
    UNDERANGE = 42
    DEFAULT = 43


class ParamType(Enum):
    valparamType = 1
    varparamType = 2


class NodeKind(Enum):
    ProK = 1
    PheadK = 2
    DecK = 3
    TypeK = 4
    VarK = 5
    ProcDecK = 6
    StmLK = 7
    StmtK = 8
    ExpK = 9


class DecKind(Enum):
    ArrayK = 1
    CharK = 2
    IntegerK = 3
    RecordK = 4
    IdK = 5


class StmtKind(Enum):
    IfK = 1
    WhileK = 2
    AssignK = 3
    ReadK = 4
    WriteK = 5
    CallK = 6
    ReturnK = 7


class ExpKind(Enum):
    OpK = 1
    ConstK = 2
    VariK = 3


class VarKind(Enum):
    IdV = 1
    ArrayMembV = 2
    FieldMembV = 3


class ExpType(Enum):
    Void = 1
    Integer = 2
    Boolean = 3


class ParamType(Enum):
    valparamType = 1
    varparamType = 2


class AccessKind(Enum):
    dir = 1
    indir = 2


class IdKind(Enum):
    typeKind = 1
    varKind = 2
    procKind = 3


class AttributeIR:
    def __init__(self):
        self.idtype = None
        self.kind = None
        self.More = {
            "VarAttr": {
                "access": None,
                "level": 0,
                "off": 0,
                "isParam": False
            },
            "ProcAttr": {
                "level": 0,
                "param": None,
                "mOff": 0,
                "nOff": 0,
                "procEntry": 0,
                "codeEntry": 0
            }
        }


class TypeKind(Enum):
    intTy = 1
    charTy = 2
    arrayTy = 3
    recordTy = 4
    boolTy = 5


class fieldchain():
    def __init__(self):
        self.id = [] * 10
        self.off = None
        self.UnitType = None
        self.Next = None


def newStmtNode(kind=None):
    t = TreeNode(NodeKind.StmtK)
    t.kind["stmt"] = kind
    return t


def newExpNode(kind):
    t = TreeNode(NodeKind.ExpK)
    t.kind["exp"] = kind
    t.attr["ExpAttr"]["varkind"] = VarKind.IdV
    t.attr["ExpAttr"]["type"] = ExpType.Void
    return t


class TypeIR():
    def __init__(self):
        self.size = 0
        self.kind = None
        self.More = \
            {
                "ArrayAttr": {"indexTy": None, "elemTy": None, "low": 0, "up": 0},
                "body": None
            }


class IONode:
    def __init__(self):
        self.input_file = None
        self.output_file = None

    def printWord(self, s):
        print(s, file=self.output_file, end='')

    def printName(self, node):
        for i in range(0, node.idnum):
            self.printWord(node.name[i] + " ")

    def printRoot(self, node, file=None):
        if file != None:
            self.output_file = open(file, 'w')
            self.picroot(node)
            self.output_file.close()
            self.output_file = None
        else:
            self.picroot(node)

    def picroot(self, node, depth=1):
        if depth == 0:
            indented = ''
        else:
            indented = '\t' * (depth - 1)
        while node is not None:
            self.printWord(indented)
            if node.nodeKind == NodeKind.ProK:
                self.printWord("Prok ")
            elif node.nodeKind == NodeKind.PheadK:
                self.printWord("PheadK ")
                self.printWord(node.name[0] + " ")
            elif node.nodeKind == NodeKind.DecK:
                self.printWord("Deck ")

                if node.kind["dec"] == DecKind.ArrayK:
                    self.printWord("ArrayK ")
                    self.printName(node)
                    self.printWord(str(node.attr["ArrayAttr"]["low"]) + " ")
                    self.printWord(str(node.attr["ArrayAttr"]["up"]) + " ")
                    if node.attr["ArrayAttr"]["childtype"] == DecKind.CharK:
                        self.printWord("Chark ")
                    elif node.attr["ArrayAttr"]["childtype"] == DecKind.IntegerK:
                        self.printWord("IntegerK ")
                elif node.kind["dec"] == DecKind.CharK:
                    self.printWord("CharK ")
                    self.printName(node)
                elif node.kind["dec"] == DecKind.IntegerK:
                    self.printWord("IntegerK ")
                    self.printName(node)
                elif node.kind["dec"] == DecKind.RecordK:
                    self.printWord("RecordK ")
                    self.printName(node)
                elif node.kind["dec"] == DecKind.IdK:
                    self.printWord("IdK ")
                    self.printWord(node.attr["type_name"] + " ")
                    self.printName(node)
                else:
                    self.printWord("error1!")

                if node.attr["ProcAttr"]["paramt"] == ParamType.varparamType:
                    self.printWord("varparam ")
                if node.attr["ProcAttr"]["paramt"] == ParamType.valparamType:
                    self.printWord("valparam ")

            elif node.nodeKind == NodeKind.TypeK:
                self.printWord("TypeK ")

            elif node.nodeKind == NodeKind.VarK:
                self.printWord("VarK ")
                if node.table[0] != None:
                    self.printWord(str(node.table[0].attrIR["More"]["VarAttr"]["off"]) + "  " + \
                                   str(node.table[0].attrIR["More"]["VarAttr"]["level"]) + "  ")

            elif node.nodeKind == NodeKind.ProcDecK:
                self.printWord("ProcDeck ")
                self.printWord(node.name[0] + " ")
                if node.table[0] != None:
                    self.printWord(str(node.table[0].attrIR["More"]["ProcAttr"]["mOff"]) + "  " + \
                                   str(node.table[0].attrIR["More"]["ProcAttr"]["nOff"]) + "  " + \
                                   str(node.table[0].attrIR["More"]["ProcAttr"]["nOff"]) + "  ")

            elif node.nodeKind == NodeKind.StmLK:
                self.printWord("StmLK ")

            elif node.nodeKind == NodeKind.StmtK:
                self.printWord("StmtK ")

                if node.kind["stmt"] == StmtKind.IfK:
                    self.printWord("IfK ")
                elif node.kind["stmt"] == StmtKind.WhileK:
                    self.printWord("WhileK ")
                elif node.kind["stmt"] == StmtKind.AssignK:
                    self.printWord("AssignK ")
                elif node.kind["stmt"] == StmtKind.ReadK:
                    self.printWord("ReadK ")
                    self.printWord(node.name[0] + "  ")
                    if node.table[0] != None:
                        self.printWord(str(node.table[0].attrIR["More"]["VarAttr"]["off"]) + "  " + \
                                       str(node.table[0].attrIR["More"]["VarAttr"]["level"]) + "  ")
                elif node.kind["stmt"] == StmtKind.WriteK:
                    self.printWord("WriteK ")
                elif node.kind["stmt"] == StmtKind.CallK:
                    self.printWord("CallK ")
                    self.printWord(node.name[0] + " ")
                elif node.kind["stmt"] == StmtKind.ReturnK:
                    self.printWord("ReturnK ")
                else:
                    self.printWord("error2!")
            elif node.nodeKind == NodeKind.ExpK:
                self.printWord("ExpK ")
                if node.kind["exp"] == ExpKind.OpK:
                    self.printWord("OpK ")
                    if node.attr["ExpAttr"]["op"] == LexType.EQ:
                        self.printWord("= ")
                    elif node.attr["ExpAttr"]["op"] == LexType.LT:
                        self.printWord("< ")
                    elif node.attr["ExpAttr"]["op"] == LexType.PLUS:
                        self.printWord("+ ")
                    elif node.attr["ExpAttr"]["op"] == LexType.TIMES:
                        self.printWord("* ")
                    elif node.attr["ExpAttr"]["op"] == LexType.MINUS:
                        self.printWord("- ")
                    elif node.attr["ExpAttr"]["op"] == LexType.OVER:
                        self.printWord("/ ")
                    else:
                        self.printWord("error3!")

                elif node.kind["exp"] == ExpKind.ConstK:
                    self.printWord("ConstK ")
                    self.printWord(str(node.attr["ExpAttr"]["val"]) + " ")

                elif node.kind["exp"] == ExpKind.VariK:
                    # self.printWord("Vari  ")
                    if node.attr["ExpAttr"]["varkind"] == VarKind.IdV:
                        self.printWord("IdK ")
                        self.printWord(node.name[0] + " ")
                        self.printWord("IdV ")
                    elif node.attr["ExpAttr"]["varkind"] == VarKind.FieldMembV:
                        self.printWord("IdK ")
                        self.printWord(node.name[0] + " ")
                        self.printWord("FieldMembV ")
                    elif node.attr["ExpAttr"]["varkind"] == VarKind.ArrayMembV:
                        self.printWord("IdK ")
                        self.printWord(node.name[0] + " ")
                        self.printWord("ArrayMembV ")
                    else:
                        self.printWord("var type error!")

                    if node.table[0] != None:
                        self.printWord(node.table[0].attrIR["More"]["VarAttr"]["off"] + "  " + \
                                       node.table[0].attrIR["More"]["VarAttr"]["level"] + "  ")

                else:
                    self.printWord("error4!")

            else:
                self.printWord("error5!")
            self.printWord(str(node.linePos) + " " + str(node.colPos) + " ")
            self.printWord('\n')
            for i in range(3):
                self.picroot(node.child[i], depth=depth + 1)
            node = node.brother

    def loadroot(self, input_path):
        file = open(input_path, 'r')
        prock_flag = False
        pre_indented = -1
        pre_root = TreeNode()
        cur = pre_root
        for line in file.readlines():
            cur_indented = line.count('\t')
            word = line.split()
            node = TreeNode()
            colPos = int(word.pop())
            linePos = int(word.pop())
            nodetype = word[0]
            if cur_indented <= 1 and prock_flag is True:
                prock_flag = False

            if nodetype == "Prok":
                node.nodeKind = NodeKind.ProK
            elif nodetype == "PheadK":
                node.nodeKind = NodeKind.PheadK
                node.insertname(word[1])
            elif nodetype == "Deck":
                node.nodeKind = NodeKind.DecK

                if word[-1] == "varparam":
                    node.attr["ProcAttr"]["paramt"] = ParamType.varparamType
                    word.pop()
                elif word[-1] == "valparam":
                    node.attr["ProcAttr"]["paramt"] = ParamType.valparamType
                    word.pop()

                if word[1] == "ArrayK":
                    node.kind["dec"] = DecKind.ArrayK
                    for name in word[2: -3]:
                        node.insertname(name)
                    node.attr["ArrayAttr"]["low"] = int(word[-3])
                    node.attr["ArrayAttr"]["up"] = int(word[-2])
                    if word[-1] == "Chark":
                        node.attr["ArrayAttr"]["childtype"] = DecKind.CharK
                    elif word[-1] == "IntegerK":
                        node.attr["ArrayAttr"]["childtype"] = DecKind.IntegerK
                elif word[1] == "IdK":
                    node.kind["dec"] = DecKind.IdK
                    node.attr["type_name"] = word[2]
                    for name in word[3:]:
                        node.insertname(name)
                else:
                    if word[1] == "CharK":
                        node.kind["dec"] = DecKind.CharK
                    elif word[1] == "IntegerK":
                        node.kind["dec"] = DecKind.IntegerK
                    elif word[1] == "RecordK":
                        node.kind["dec"] = DecKind.RecordK
                    else:
                        print("wrong11")
                    for name in word[2:]:
                        node.insertname(name)

            elif nodetype == "TypeK":
                node.nodeKind = NodeKind.TypeK
            elif nodetype == "VarK":
                node.nodeKind = NodeKind.VarK
            elif nodetype == "ProcDeck":
                node.nodeKind = NodeKind.ProcDecK
                node.insertname(word[1])
                prock_flag = True
            elif nodetype == "StmLK":
                node.nodeKind = NodeKind.StmLK
            elif nodetype == "StmtK":
                node = newStmtNode()
                # node.nodeKind = NodeKind.StmtK

                if word[1] == "IfK":
                    node.kind["stmt"] = StmtKind.IfK
                elif word[1] == "WhileK":
                    node.kind["stmt"] = StmtKind.WhileK
                elif word[1] == "AssignK":
                    node.kind["stmt"] = StmtKind.AssignK
                elif word[1] == "ReadK":
                    node.kind["stmt"] = StmtKind.ReadK
                    node.insertname(word[2])
                elif word[1] == "WriteK":
                    node.kind["stmt"] = StmtKind.WriteK
                elif word[1] == "CallK":
                    node.kind["stmt"] = StmtKind.CallK
                elif word[1] == "ReturnK":
                    node.kind["stmt"] = StmtKind.ReturnK
                else:
                    print("wrong12")

            elif nodetype == "ExpK":
                node = newExpNode(None)
                if word[1] == "OpK":
                    node.kind["exp"] = ExpKind.OpK
                    if word[2] == '=':
                        node.attr["ExpAttr"]["op"] = LexType.EQ
                    elif word[2] == '<':
                        node.attr["ExpAttr"]["op"] = LexType.LT
                    elif word[2] == '+':
                        node.attr["ExpAttr"]["op"] = LexType.PLUS
                    elif word[2] == '*':
                        node.attr["ExpAttr"]["op"] = LexType.TIMES
                    elif word[2] == '-':
                        node.attr["ExpAttr"]["op"] = LexType.MINUS
                    elif word[2] == '/':
                        node.attr["ExpAttr"]["op"] = LexType.OVER

                elif word[1] == "ConstK":
                    node.kind["exp"] = ExpKind.ConstK
                    node.attr["ExpAttr"]["val"] = int(word[2])

                elif word[1] == "IdK":
                    node.kind["exp"] = ExpKind.VariK
                    for name in word[2: -1]:
                        node.insertname(name)
                    if word[-1] == "IdV":
                        node.attr["ExpAttr"]["varkind"] = VarKind.IdV
                    if word[-1] == "FieldMembV":
                        node.attr["ExpAttr"]["varkind"] = VarKind.FieldMembV
                    if word[-1] == "ArrayMembV":
                        node.attr["ExpAttr"]["varkind"] = VarKind.ArrayMembV

            if cur_indented == 1:
                cur = pre_root.child[0]
                node.father = cur
                if node.nodeKind == NodeKind.PheadK:
                    cur.child[0] = node
                elif node.nodeKind == NodeKind.StmLK:
                    cur.child[2] = node
                elif cur.child[1] is None:
                    cur.child[1] = node
                else:
                    cur = cur.child[1]
                    while cur.brother is not None:
                        cur = cur.brother
                    cur.brother = node
            elif prock_flag is True and cur_indented >= 2:
                while pre_indented != cur_indented - 1:
                    pre_indented -= 1
                    cur = cur.father
                node.father = cur
                if node.nodeKind == NodeKind.DecK:
                    if cur.child[0] is None:
                        cur.child[0] = node
                    else:
                        cur.child[0].addbrother(node)
                elif node.nodeKind == NodeKind.StmLK:
                    cur.child[2] = node
                    node.father = cur
                else:
                    if cur.child[1] is None:
                        cur.child[1] = node
                    else:
                        cur.child[1].addbrother(node)

            elif cur_indented == pre_indented + 1:
                node.father = cur
                cur.child[0] = node
            elif cur_indented <= pre_indented:
                store_indented = pre_indented
                while cur_indented != store_indented:
                    cur = cur.father
                    store_indented -= 1
                node.father = cur.father
                if (cur.father.kind["stmt"] == StmtKind.AssignK or cur.father.kind["exp"] == ExpKind.OpK) and \
                        cur.father.child[0] is not None:
                    cur.father.child[1] = node
                elif cur.father.kind["stmt"] == StmtKind.CallK and cur.father.child[1] is None:
                    cur.father.child[1] = node
                else:
                    cur.brother = node
            pre_indented = cur_indented
            cur = node

            node.linePos = linePos
            node.colPos = colPos
        file.close()
        return pre_root.child[0]


class TreeNode:
    def __init__(self, nodeKind=None):
        self.father = None
        self.brother = None
        self.child = [None, None, None]
        self.linePos = 0
        self.colPos = 0
        self.kind = {"dec": None, "stmt": None, "exp": None}
        self.nodeKind = nodeKind
        self.idnum = 0
        self.name = [''] * 10
        self.table = [None] * 10
        self.attr = \
            {
                "ArrayAttr": {"low": 0, "up": 0, "childtype": None},
                "ProcAttr": {"paramt": None},
                "ExpAttr": {"op": None, "val": 0, "varkind": None, "type": None},
                "type_name": ""
            }
        self.file = None

    def insertname(self, s):
        self.name[self.idnum] = s
        self.idnum += 1

    def add(self, TreeNode):
        self.child.append(TreeNode)

    def get(self, id):
        return self.child[id]

    def addbrother(self, br):
        cur = self
        br.father = cur.father
        while cur.brother is not None:
            cur = cur.brother
        cur.brother = br


class ParamTable:
    def __init__(self):
        entry = SymTableItem()
        next = None


class SymTableItem:
    def __init__(self):
        self.idName = ""
        self.attrIR = AttributeIR()
        self.next = None


def NewTy(kind):
    table = TypeIR()
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
