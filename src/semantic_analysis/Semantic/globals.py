
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


class ParamTable():
    def __init__(self):
        entry = Symbtable()
        next = ParamTable()


class AttributeIR():
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


class Symbtable():
    def __init__(self):
        self.idName = ""
        self.attrIR = AttributeIR()
        self.next = None


class Token():
    def __init__(self, line=0, lex=LexType.DEFAULT, sem=None):
        self.line = line
        self.lex = lex
        self.sem = sem

    def setLine(self, line):
        self.line = line

    def setLex(self, lex):
        self.lex = lex

    def setSem(self, sem):
        self.sem = sem

    def toString(self):
        if self.sem != None:
            return "<" + str(self.line) + "," + self.lex.name + "," + str(self.sem) + ">"
        else:
            return "<" + str(self.line) + "," + self.lex.name + ">"


class Log():
    def e(self, tag, word):
        sys.stderr.write("[error] from " + tag + " " + word + "\n")


    def d(self, tag, word):
        sys.stdout.write("[log] from " + tag + " " + word + "\n")


class TreeNode:
    def __init__(self, nodeKind=None):
        self.father = None
        self.brother = None
        self.child = [None, None, None]
        self.linePos = 0
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

    def printname(self):
        for i in range(0, self.idnum):
            printWord(self.name[i] + " ")



def printWord(s):
    print(s, file=None, end='')

def pictmp(node, depth=1):
    if depth == 0:
        indented = ''
    else:
        indented = '\t' * (depth - 1)
    while node is not None:
        print(node.nodeKind, node.name[0])
        for i in range(3):
            pictmp(node.child[i], depth=depth+1)
        node = node.brother

def picroot(node, depth=1, s=None, file=None):
    if depth == 0:
        indented = ''
    else:
        indented = '\t' * (depth - 1)
    while node is not None:
        printWord(indented)
        if node.nodeKind == NodeKind.ProK:
            printWord("Prok ")
        elif node.nodeKind == NodeKind.PheadK:
            printWord("PheadK  ")
            printWord(node.name[0] + "  ")
        elif node.nodeKind == NodeKind.DecK:
            printWord("Deck ")

            if node.kind["dec"] == DecKind.ArrayK:
                printWord("ArrayK ")
                node.printname()
                printWord(str(node.attr["ArrayAttr"]["low"]) + " ")
                printWord(str(node.attr["ArrayAttr"]["up"]) + " ")
                if node.attr["ArrayAttr"]["childtype"] == DecKind.CharK:
                    printWord("Chark ")
                elif node.attr["ArrayAttr"]["childtype"] == DecKind.IntegerK:
                    printWord("IntegerK ")
            elif node.kind["dec"] == DecKind.CharK:
                printWord("CharK ")
                node.printname()
            elif node.kind["dec"] == DecKind.IntegerK:
                printWord("IntegerK ")
                node.printname()
            elif node.kind["dec"] == DecKind.RecordK:
                printWord("RecordK ")
                node.printname()
            elif node.kind["dec"] == DecKind.IdK:
                printWord("IdK ")
                printWord(node.attr["type_name"] + " ")
                node.printname()
            else:
                printWord("error1!")

            if node.attr["ProcAttr"]["paramt"] == ParamType.varparamType:
                printWord("varparam ")
            if node.attr["ProcAttr"]["paramt"] == ParamType.valparamType:
                printWord("valparam ")

        elif node.nodeKind == NodeKind.TypeK:
            printWord("TypeK ")

        elif node.nodeKind == NodeKind.VarK:
            printWord("VarK ")
            if node.table[0] != None:
                printWord(str(node.table[0].attrIR["More"]["VarAttr"]["off"]) + "  " + \
                          str(node.table[0].attrIR["More"]["VarAttr"]["level"]) + "  ")

        elif node.nodeKind == NodeKind.ProcDecK:
            printWord("ProcDeck ")
            printWord(node.name[0] + "  ")
            if node.table[0] != None:
                printWord(str(node.table[0].attrIR["More"]["ProcAttr"]["mOff"]) + "  " + \
                          str(node.table[0].attrIR["More"]["ProcAttr"]["nOff"]) + "  " + \
                          str(node.table[0].attrIR["More"]["ProcAttr"]["nOff"]) + "  ")

        elif node.nodeKind == NodeKind.StmLK:
            printWord("StmLK ")

        elif node.nodeKind == NodeKind.StmtK:
            printWord("StmtK ")

            if node.kind["stmt"] == StmtKind.IfK:
                printWord("IfK ")
            elif node.kind["stmt"] == StmtKind.WhileK:
                printWord("WhileK ")
            elif node.kind["stmt"] == StmtKind.AssignK:
                printWord("AssignK ")
            elif node.kind["stmt"] == StmtKind.ReadK:
                printWord("ReadK ")
                printWord(node.name[0] + "  ")
                if node.table[0] != None:
                    printWord(str(node.table[0].attrIR["More"]["VarAttr"]["off"]) + "  " + \
                              str(node.table[0].attrIR["More"]["VarAttr"]["level"]) + "  ")
            elif node.kind["stmt"] == StmtKind.WriteK:
                printWord("WriteK ")
            elif node.kind["stmt"] == StmtKind.CallK:
                printWord("CallK ")
                printWord(node.name[0] + " ")
            elif node.kind["stmt"] == StmtKind.ReturnK:
                printWord("ReturnK ")
            else:
                printWord("error2!")
        elif node.nodeKind == NodeKind.ExpK:
            printWord("ExpK ")
            if node.kind["exp"] == ExpKind.OpK:
                printWord("OpK ")
                if node.attr["ExpAttr"]["op"] == LexType.EQ:
                    printWord("= ")
                elif node.attr["ExpAttr"]["op"] == LexType.LT:
                    printWord("< ")
                elif node.attr["ExpAttr"]["op"] == LexType.PLUS:
                    printWord("+ ")
                elif node.attr["ExpAttr"]["op"] == LexType.TIMES:
                    printWord("* ")
                elif node.attr["ExpAttr"]["op"] == LexType.MINUS:
                    printWord("- ")
                elif node.attr["ExpAttr"]["op"] == LexType.OVER:
                    printWord("/ ")
                else:
                    printWord("error3!")

            elif node.kind["exp"] == ExpKind.ConstK:
                printWord("ConstK ")
                printWord(str(node.attr["ExpAttr"]["val"]) + " ")

            elif node.kind["exp"] == ExpKind.VariK:
                #printWord("Vari  ")
                if node.attr["ExpAttr"]["varkind"] == VarKind.IdV:
                    printWord("IdK ")
                    printWord(node.name[0] + " ")
                    printWord("IdV ")
                elif node.attr["ExpAttr"]["varkind"] == VarKind.FieldMembV:
                    printWord("IdK ")
                    printWord(node.name[0] + " ")
                    printWord("FieldMembV ")
                elif node.attr["ExpAttr"]["varkind"] == VarKind.ArrayMembV:
                    printWord("IdK ")
                    printWord(node.name[0] + " ")
                    printWord("ArrayMembV ")
                else:
                    printWord("var type error!")


                if node.table[0] != None:
                    printWord(node.table[0].attrIR["More"]["VarAttr"]["off"] + "  " + \
                              node.table[0].attrIR["More"]["VarAttr"]["level"] + "  ")

            else:
                printWord("error4!")

        else:
            printWord("error5!")
        printWord('\n')
        for i in range(3):
            picroot(node.child[i], depth=depth+1, s=node.nodeKind)
        node = node.brother


def loadroot():
    file = open('tmp.txt', 'r')
    prock_flag = False
    pre_indented = -1
    pre_root = TreeNode()
    cur = pre_root
    for line in file.readlines():
        cur_indented = line.count('\t')
        word = line.split()
        node = TreeNode()
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
            #node.nodeKind = NodeKind.StmtK

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
                node.attr["ExpAttr"]["val"] = int(word[3])

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
        elif prock_flag is True and cur_indented == 2:
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
            if (cur.father.kind["stmt"] == StmtKind.AssignK or cur.father.kind["exp"] == ExpKind.OpK) and cur.father.child[0] is not None:
                cur.father.child[1] = node
            elif cur.father.kind["stmt"] == StmtKind.CallK and cur.father.child[1] is None:
                cur.father.child[1] = node
            else:
                cur.brother = node
        pre_indented = cur_indented
        cur = node

    file.close()
    return pre_root.child[0]

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


def newRootNode():
    return TreeNode(NodeKind.ProK)


def newPheadNode():
    return TreeNode(NodeKind.PheadK)


def newDecANode(kind):
    return TreeNode(kind)


def newDecNode():
    return TreeNode(NodeKind.DecK)


def newProcNode():
    return TreeNode(NodeKind.ProcDecK)


def newStmtNode(kind=None):
    t = TreeNode(NodeKind.StmtK)
    t.kind["stmt"] = kind
    return t


def newStmlNode():
    t = TreeNode(NodeKind.StmLK)
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
                "ArrayAttr":{"indexTy":None,"elemTy":None,"low":0,"up":0},
                "body":None
            }

#scope = [0] *1000
#Level = None
#Off = None
INITOFF = 7
SCOPESIZE = 1000
savedOff = None
Error = None