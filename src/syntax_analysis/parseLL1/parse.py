import json
from LL1Support import *
# from src.syntax_analysis.parseLL1.LL1Support import *

class LL1Table:
    def __init__(self):
        self.Table = {}
        self.initTable()
        self.Table[NontmlType.Program][LexType.PROGRAM] = 1

        self.Table[NontmlType.ProgramHead][LexType.PROGRAM] = 2

        self.Table[NontmlType.ProgramName][LexType.ID] = 3

        self.Table[NontmlType.DeclarePart][LexType.TYPE] = 4
        self.Table[NontmlType.DeclarePart][LexType.VAR] = 4
        self.Table[NontmlType.DeclarePart][LexType.PROCEDURE] = 4
        self.Table[NontmlType.DeclarePart][LexType.BEGIN] = 4

        self.Table[NontmlType.TypeDec][LexType.VAR] = 5
        self.Table[NontmlType.TypeDec][LexType.PROCEDURE] = 5
        self.Table[NontmlType.TypeDec][LexType.BEGIN] = 5

        self.Table[NontmlType.TypeDec][LexType.TYPE] = 6

        self.Table[NontmlType.TypeDeclaration][LexType.TYPE] = 7

        self.Table[NontmlType.TypeDecList][LexType.ID] = 8

        self.Table[NontmlType.TypeDecMore][LexType.VAR] = 9
        self.Table[NontmlType.TypeDecMore][LexType.PROCEDURE] = 9
        self.Table[NontmlType.TypeDecMore][LexType.BEGIN] = 9

        self.Table[NontmlType.TypeDecMore][LexType.ID] = 10

        self.Table[NontmlType.TypeId][LexType.ID] = 11

        self.Table[NontmlType.TypeName][LexType.INTEGER] = 12
        self.Table[NontmlType.TypeName][LexType.CHAR] = 12

        self.Table[NontmlType.TypeName][LexType.ARRAY] = 13
        self.Table[NontmlType.TypeName][LexType.RECORD] = 13

        self.Table[NontmlType.TypeName][LexType.ID] = 14

        self.Table[NontmlType.BaseType][LexType.INTEGER] = 15

        self.Table[NontmlType.BaseType][LexType.CHAR] = 16

        self.Table[NontmlType.StructureType][LexType.ARRAY] = 17

        self.Table[NontmlType.StructureType][LexType.RECORD] = 18

        self.Table[NontmlType.ArrayType][LexType.ARRAY] = 19

        self.Table[NontmlType.Low][LexType.INTC] = 20

        self.Table[NontmlType.Top][LexType.INTC] = 21

        self.Table[NontmlType.RecType][LexType.RECORD] = 22

        self.Table[NontmlType.FieldDecList][LexType.INTEGER] = 23
        self.Table[NontmlType.FieldDecList][LexType.CHAR] = 23

        self.Table[NontmlType.FieldDecList][LexType.ARRAY] = 24

        self.Table[NontmlType.FieldDecMore][LexType.END] = 25

        self.Table[NontmlType.FieldDecMore][LexType.INTEGER] = 26
        self.Table[NontmlType.FieldDecMore][LexType.CHAR] = 26
        self.Table[NontmlType.FieldDecMore][LexType.ARRAY] = 26

        self.Table[NontmlType.IdList][LexType.ID] = 27

        self.Table[NontmlType.IdMore][LexType.SEMI] = 28

        self.Table[NontmlType.IdMore][LexType.COMMA] = 29

        self.Table[NontmlType.VarDec][LexType.PROCEDURE] = 30
        self.Table[NontmlType.VarDec][LexType.BEGIN] = 30

        self.Table[NontmlType.VarDec][LexType.VAR] = 31

        self.Table[NontmlType.VarDeclaration][LexType.VAR] = 32

        self.Table[NontmlType.VarDecList][LexType.INTEGER] = 33
        self.Table[NontmlType.VarDecList][LexType.CHAR] = 33
        self.Table[NontmlType.VarDecList][LexType.ARRAY] = 33
        self.Table[NontmlType.VarDecList][LexType.RECORD] = 33
        self.Table[NontmlType.VarDecList][LexType.ID] = 33

        self.Table[NontmlType.VarDecMore][LexType.PROCEDURE] = 34
        self.Table[NontmlType.VarDecMore][LexType.BEGIN] = 34

        self.Table[NontmlType.VarDecMore][LexType.INTEGER] = 35
        self.Table[NontmlType.VarDecMore][LexType.CHAR] = 35
        self.Table[NontmlType.VarDecMore][LexType.ARRAY] = 35
        self.Table[NontmlType.VarDecMore][LexType.RECORD] = 35
        self.Table[NontmlType.VarDecMore][LexType.ID] = 35

        self.Table[NontmlType.VarIdList][LexType.ID] = 36

        self.Table[NontmlType.VarIdMore][LexType.SEMI] = 37

        self.Table[NontmlType.VarIdMore][LexType.COMMA] = 38

        self.Table[NontmlType.ProcDec][LexType.BEGIN] = 39

        self.Table[NontmlType.ProcDec][LexType.PROCEDURE] = 40

        self.Table[NontmlType.ProcDeclaration][LexType.PROCEDURE] = 41

        self.Table[NontmlType.ProcDecMore][LexType.BEGIN] = 42

        self.Table[NontmlType.ProcDecMore][LexType.PROCEDURE] = 43

        self.Table[NontmlType.ProcName][LexType.ID] = 44

        self.Table[NontmlType.ParamList][LexType.RPAREN] = 45

        self.Table[NontmlType.ParamList][LexType.INTEGER] = 46
        self.Table[NontmlType.ParamList][LexType.CHAR] = 46
        self.Table[NontmlType.ParamList][LexType.ARRAY] = 46
        self.Table[NontmlType.ParamList][LexType.RECORD] = 46
        self.Table[NontmlType.ParamList][LexType.ID] = 46
        self.Table[NontmlType.ParamList][LexType.VAR] = 46

        self.Table[NontmlType.ParamDecList][LexType.INTEGER] = 47
        self.Table[NontmlType.ParamDecList][LexType.CHAR] = 47
        self.Table[NontmlType.ParamDecList][LexType.ARRAY] = 47
        self.Table[NontmlType.ParamDecList][LexType.RECORD] = 47
        self.Table[NontmlType.ParamDecList][LexType.ID] = 47
        self.Table[NontmlType.ParamDecList][LexType.VAR] = 47

        self.Table[NontmlType.ParamMore][LexType.RPAREN] = 48

        self.Table[NontmlType.ParamMore][LexType.SEMI] = 49

        self.Table[NontmlType.Param][LexType.INTEGER] = 50
        self.Table[NontmlType.Param][LexType.CHAR] = 50
        self.Table[NontmlType.Param][LexType.ARRAY] = 50
        self.Table[NontmlType.Param][LexType.RECORD] = 50
        self.Table[NontmlType.Param][LexType.ID] = 50

        self.Table[NontmlType.Param][LexType.VAR] = 51

        self.Table[NontmlType.FormList][LexType.ID] = 52

        self.Table[NontmlType.FidMore][LexType.SEMI] = 53
        self.Table[NontmlType.FidMore][LexType.RPAREN] = 53

        self.Table[NontmlType.FidMore][LexType.COMMA] = 54

        self.Table[NontmlType.ProcDecPart][LexType.TYPE] = 55
        self.Table[NontmlType.ProcDecPart][LexType.VAR] = 55
        self.Table[NontmlType.ProcDecPart][LexType.PROCEDURE] = 55
        self.Table[NontmlType.ProcDecPart][LexType.BEGIN] = 55

        self.Table[NontmlType.ProcBody][LexType.BEGIN] = 56

        self.Table[NontmlType.ProgramBody][LexType.BEGIN] = 57

        self.Table[NontmlType.StmList][LexType.ID] = 58
        self.Table[NontmlType.StmList][LexType.IF] = 58
        self.Table[NontmlType.StmList][LexType.WHILE] = 58
        self.Table[NontmlType.StmList][LexType.RETURN] = 58
        self.Table[NontmlType.StmList][LexType.READ] = 58
        self.Table[NontmlType.StmList][LexType.WRITE] = 58

        self.Table[NontmlType.StmMore][LexType.END] = 59
        self.Table[NontmlType.StmMore][LexType.ENDWH] = 59
        self.Table[NontmlType.StmMore][LexType.ELSE] = 59
        self.Table[NontmlType.StmMore][LexType.FI] = 59

        self.Table[NontmlType.StmMore][LexType.SEMI] = 60

        self.Table[NontmlType.Stm][LexType.IF] = 61

        self.Table[NontmlType.Stm][LexType.WHILE] = 62

        self.Table[NontmlType.Stm][LexType.READ] = 63

        self.Table[NontmlType.Stm][LexType.WRITE] = 64

        self.Table[NontmlType.Stm][LexType.RETURN] = 65

        self.Table[NontmlType.Stm][LexType.ID] = 66

        self.Table[NontmlType.AssCall][LexType.ASSIGN] = 67
        self.Table[NontmlType.AssCall][LexType.LMIDPAREN] = 67
        self.Table[NontmlType.AssCall][LexType.DOT] = 67

        self.Table[NontmlType.AssCall][LexType.LPAREN] = 68

        self.Table[NontmlType.AssignmentRest][LexType.ASSIGN] = 69
        self.Table[NontmlType.AssignmentRest][LexType.LMIDPAREN] = 69
        self.Table[NontmlType.AssignmentRest][LexType.DOT] = 69

        self.Table[NontmlType.ConditionalStm][LexType.IF] = 70

        self.Table[NontmlType.LoopStm][LexType.WHILE] = 71

        self.Table[NontmlType.InputStm][LexType.READ] = 72

        self.Table[NontmlType.InVar][LexType.ID] = 73

        self.Table[NontmlType.OutputStm][LexType.WRITE] = 74

        self.Table[NontmlType.ReturnStm][LexType.RETURN] = 75

        self.Table[NontmlType.CallStmRest][LexType.LPAREN] = 76

        self.Table[NontmlType.ActParamList][LexType.RPAREN] = 77

        self.Table[NontmlType.ActParamList][LexType.ID] = 78
        self.Table[NontmlType.ActParamList][LexType.INTC] = 78
        self.Table[NontmlType.ActParamList][LexType.LPAREN] = 78

        self.Table[NontmlType.ActParamMore][LexType.RPAREN] = 79

        self.Table[NontmlType.ActParamMore][LexType.COMMA] = 80

        self.Table[NontmlType.RelExp][LexType.LPAREN] = 81
        self.Table[NontmlType.RelExp][LexType.INTC] = 81
        self.Table[NontmlType.RelExp][LexType.ID] = 81

        self.Table[NontmlType.OtherRelE][LexType.LT] = 82
        self.Table[NontmlType.OtherRelE][LexType.EQ] = 82

        self.Table[NontmlType.Exp][LexType.LPAREN] = 83
        self.Table[NontmlType.Exp][LexType.INTC] = 83
        self.Table[NontmlType.Exp][LexType.ID] = 83

        self.Table[NontmlType.OtherTerm][LexType.LT] = 84
        self.Table[NontmlType.OtherTerm][LexType.EQ] = 84
        self.Table[NontmlType.OtherTerm][LexType.THEN] = 84
        self.Table[NontmlType.OtherTerm][LexType.DO] = 84
        self.Table[NontmlType.OtherTerm][LexType.RPAREN] = 84
        self.Table[NontmlType.OtherTerm][LexType.END] = 84
        self.Table[NontmlType.OtherTerm][LexType.SEMI] = 84
        self.Table[NontmlType.OtherTerm][LexType.COMMA] = 84
        self.Table[NontmlType.OtherTerm][LexType.ENDWH] = 84
        self.Table[NontmlType.OtherTerm][LexType.ELSE] = 84
        self.Table[NontmlType.OtherTerm][LexType.FI] = 84
        self.Table[NontmlType.OtherTerm][LexType.RMIDPAREN] = 84

        self.Table[NontmlType.OtherTerm][LexType.PLUS] = 85
        self.Table[NontmlType.OtherTerm][LexType.MINUS] = 85

        self.Table[NontmlType.Term][LexType.LPAREN] = 86
        self.Table[NontmlType.Term][LexType.INTC] = 86
        self.Table[NontmlType.Term][LexType.ID] = 86

        self.Table[NontmlType.OtherFactor][LexType.PLUS] = 87
        self.Table[NontmlType.OtherFactor][LexType.MINUS] = 87
        self.Table[NontmlType.OtherFactor][LexType.LT] = 87
        self.Table[NontmlType.OtherFactor][LexType.EQ] = 87
        self.Table[NontmlType.OtherFactor][LexType.THEN] = 87
        self.Table[NontmlType.OtherFactor][LexType.ELSE] = 87
        self.Table[NontmlType.OtherFactor][LexType.FI] = 87
        self.Table[NontmlType.OtherFactor][LexType.DO] = 87
        self.Table[NontmlType.OtherFactor][LexType.ENDWH] = 87
        self.Table[NontmlType.OtherFactor][LexType.RPAREN] = 87
        self.Table[NontmlType.OtherFactor][LexType.END] = 87
        self.Table[NontmlType.OtherFactor][LexType.SEMI] = 87
        self.Table[NontmlType.OtherFactor][LexType.COMMA] = 87
        self.Table[NontmlType.OtherFactor][LexType.RMIDPAREN] = 87

        self.Table[NontmlType.OtherFactor][LexType.TIMES] = 88
        self.Table[NontmlType.OtherFactor][LexType.OVER] = 88

        self.Table[NontmlType.Factor][LexType.LPAREN] = 89

        self.Table[NontmlType.Factor][LexType.INTC] = 90

        self.Table[NontmlType.Factor][LexType.ID] = 91

        self.Table[NontmlType.Variable][LexType.ID] = 92

        self.Table[NontmlType.VariMore][LexType.ASSIGN] = 93
        self.Table[NontmlType.VariMore][LexType.TIMES] = 93
        self.Table[NontmlType.VariMore][LexType.OVER] = 93
        self.Table[NontmlType.VariMore][LexType.PLUS] = 93
        self.Table[NontmlType.VariMore][LexType.MINUS] = 93
        self.Table[NontmlType.VariMore][LexType.LT] = 93
        self.Table[NontmlType.VariMore][LexType.EQ] = 93
        self.Table[NontmlType.VariMore][LexType.THEN] = 93
        self.Table[NontmlType.VariMore][LexType.ELSE] = 93
        self.Table[NontmlType.VariMore][LexType.FI] = 93
        self.Table[NontmlType.VariMore][LexType.DO] = 93
        self.Table[NontmlType.VariMore][LexType.ENDWH] = 93
        self.Table[NontmlType.VariMore][LexType.RPAREN] = 93
        self.Table[NontmlType.VariMore][LexType.END] = 93
        self.Table[NontmlType.VariMore][LexType.SEMI] = 93
        self.Table[NontmlType.VariMore][LexType.COMMA] = 93
        self.Table[NontmlType.VariMore][LexType.RMIDPAREN] = 93

        self.Table[NontmlType.VariMore][LexType.LMIDPAREN] = 94

        self.Table[NontmlType.VariMore][LexType.DOT] = 95

        self.Table[NontmlType.FieldVar][LexType.ID] = 96

        self.Table[NontmlType.FieldVarMore][LexType.ASSIGN] = 97
        self.Table[NontmlType.FieldVarMore][LexType.TIMES] = 97
        self.Table[NontmlType.FieldVarMore][LexType.OVER] = 97
        self.Table[NontmlType.FieldVarMore][LexType.PLUS] = 97
        self.Table[NontmlType.FieldVarMore][LexType.MINUS] = 97
        self.Table[NontmlType.FieldVarMore][LexType.LT] = 97
        self.Table[NontmlType.FieldVarMore][LexType.EQ] = 97
        self.Table[NontmlType.FieldVarMore][LexType.THEN] = 97
        self.Table[NontmlType.FieldVarMore][LexType.ELSE] = 97
        self.Table[NontmlType.FieldVarMore][LexType.FI] = 97
        self.Table[NontmlType.FieldVarMore][LexType.DO] = 97
        self.Table[NontmlType.FieldVarMore][LexType.ENDWH] = 97
        self.Table[NontmlType.FieldVarMore][LexType.RPAREN] = 97
        self.Table[NontmlType.FieldVarMore][LexType.END] = 97
        self.Table[NontmlType.FieldVarMore][LexType.SEMI] = 97
        self.Table[NontmlType.FieldVarMore][LexType.COMMA] = 97

        self.Table[NontmlType.FieldVarMore][LexType.LMIDPAREN] = 98

        self.Table[NontmlType.CmpOp][LexType.LT] = 99

        self.Table[NontmlType.CmpOp][LexType.EQ] = 100

        self.Table[NontmlType.AddOp][LexType.PLUS] = 101

        self.Table[NontmlType.AddOp][LexType.MINUS] = 102

        self.Table[NontmlType.MultOp][LexType.TIMES] = 103

        self.Table[NontmlType.MultOp][LexType.OVER] = 104

    def initTable(self):
        for _, k in NontmlType.__members__.items():
            self.Table[k] = {}
        for _, k in NontmlType.__members__.items():
            for _, v in LexType.__members__.items():
                self.Table[k][v] = 0

    def getPredict(self, a, b):
        return self.Table[a][b]


class LL1Parse:
    def __init__(self):
        self.stack = []
        self.stack_node = []
        self.stack_op = []
        self.stack_num = []
        self.currentP = TreeNode()
        self.currentToken = TokenType()
        self.getExpResult = True
        self.getExpResult2 = False
        self.expflag = 0 #纪录表达式中，未匹配的左括号数目
        self.saveP = None
        self.temp = None

        self.stacktopN = None
        self.stacktopT = None
        
        self.dict_seperator = {'+': "PLUS", '-': "MINUS", '*': "TIMES", '/': "OVER", '(': "LPAREN", ')': "RPAREN", '.': "DOT",
                '[': "LMIDPAREN", ']': "RMIDPAREN", ';': "SEMI", ':': "COLON", ',': "COMMA", '<': "LT", '=': "EQ"}
        self.fpnum = 0
        self.tokens = None

        self.error = []

    def getLexType(self, token):
        lex = ""
        # print(lex)
        if token["type"] == "RESERVED":
            lex = token["name"].upper()
        elif token["type"] == "SEPERATOR":
            lex = self.dict_seperator[token["name"]]
        elif token["type"] == "ID":
            lex = "ID"
        elif token["type"] == "EOF":
            lex = "ENDFILE"
        elif token["type"] == "NUMBER":
            lex = "INTC"
        elif token["type"] == "CHARC":
            lex = "CHAR"
        elif token["type"] == "UNDERANGE":
            lex = "UNDERANGE"
        elif token["type"] == "ASSIGN":
            lex = "ASSIGN"
        else:
            print("wrong")
            # print(token)
            exit(0)
        return eval("LexType." + lex)
        # error intc charc default

    def gettoken(self):
        token = TokenType()
        p = self.tokens[self.fpnum]
        token.lineshow = p['line']
        token.col = p['col']
        token.Sem = p['name']
        token.Lex = self.getLexType(p)
        # print(p)
        self.fpnum += 1
        return token

    def popNode(self, node=None):
        t, v = self.stack_node.pop()
        if node is None:
            return
        if v == -1:
            t.brother = node
        else:
            t.child[v] = node
        # print(v, node.nodeKind, t.nodeKind)

    def Priosity(self, op):
        if op == LexType.END:
            return -1
        elif op == LexType.LPAREN:
            return 0
        elif op == LexType.LT or op == LexType.EQ:
            return 1
        elif op == LexType.PLUS or op == LexType.MINUS:
            return 2
        elif op == LexType.TIMES or op == LexType.OVER:
            return 3
        else:
            self.error.append(
                "in line:{0} col{1}, {2} no this operator".format(self.currentToken.linePos, self.currentToken.colPos,
                                                       self.currentToken.Sem))

    def process1(self):
        self.stack.append(StackNode(2, LexType.DOT))
        self.stack.append(StackNode(1, NontmlType.ProgramBody))
        self.stack.append(StackNode(1, NontmlType.DeclarePart))
        self.stack.append(StackNode(1, NontmlType.ProgramHead))

    def process2(self):
        self.stack.append(StackNode(1, NontmlType.ProgramName))
        self.stack.append(StackNode(2, LexType.PROGRAM))

        self.currentP = newPheadNode()
        self.popNode(self.currentP)

    def process3(self):
        self.stack.append(StackNode(2, LexType.ID))

        self.currentP.name[0] = self.currentToken.Sem
        self.currentP.linePos = self.currentToken.lineshow
        self.currentP.colPos = self.currentToken.col
        self.currentP.idnum += 1

    def process4(self):
        self.stack.append(StackNode(1, NontmlType.ProcDec))
        self.stack.append(StackNode(1, NontmlType.VarDec))
        self.stack.append(StackNode(1, NontmlType.TypeDec))

    def process5(self):
        pass

    def process6(self):
        self.stack.append(StackNode(1, NontmlType.TypeDeclaration))

    def process7(self):
        self.stack.append(StackNode(1, NontmlType.TypeDecList))
        self.stack.append(StackNode(2, LexType.TYPE))

        self.currentP = newTypeNode()
        self.popNode(self.currentP)

        self.stack_node.append((self.currentP, -1))
        self.stack_node.append((self.currentP, 0))

    def process8(self):
        self.stack.append(StackNode(1, NontmlType.TypeDecMore))
        self.stack.append(StackNode(2, LexType.SEMI))
        self.stack.append(StackNode(1, NontmlType.TypeName))
        self.stack.append(StackNode(2, LexType.EQ))
        self.stack.append(StackNode(1, NontmlType.TypeId))

        self.currentP = newDecNode()
        self.popNode(self.currentP)

        self.stack_node.append((self.currentP, -1))

    def process9(self):
        self.stack_node.pop()

    def process10(self):
        self.stack.append(StackNode(1, NontmlType.TypeDecList))

    def process11(self):
        self.stack.append(StackNode(2, LexType.ID))
        self.currentP.name[0] = self.currentToken.Sem
        self.currentP.linePos = self.currentToken.lineshow
        self.currentP.colPos = self.currentToken.col
        self.currentP.idnum += 1

    def process12(self):
        self.stack.append(StackNode(1, NontmlType.BaseType))
        # self.currentP.kind["dec"] = self.temp
        self.tempp = (self.currentP, 1)

    def process13(self):
        self.stack.append(StackNode(1, NontmlType.StructureType))

    def process14(self):
        self.stack.append(StackNode(2, LexType.ID))
        self.currentP.kind["dec"] = DecKind.IdK
        self.currentP.attr["type_name"] = self.currentToken.Sem
        self.currentP.linePos = self.currentToken.lineshow
        self.currentP.colPos = self.currentToken.col

    def process15(self):
        self.stack.append(StackNode(2, LexType.INTEGER))
        k, v = self.tempp
        if v == 1:
            k.kind["dec"] = DecKind.IntegerK
        elif v == 2:
            k.attr["ArrayAttr"]["childtype"] = DecKind.IntegerK
        # self.temp = DecKind.IntegerK

    def process16(self):
        self.stack.append(StackNode(2, LexType.CHAR))
        k, v = self.tempp
        if v == 1:
            k.kind["dec"] = DecKind.CharK
        elif v == 2:
            k.attr["ArrayAttr"]["childtype"] = DecKind.CharK
        # self.temp = DecKind.CharK

    def process17(self):
        self.stack.append(StackNode(1, NontmlType.ArrayType))

    def process18(self):
        self.stack.append(StackNode(1, NontmlType.RecType))

    def process19(self):
        self.stack.append(StackNode(1, NontmlType.BaseType))
        self.stack.append(StackNode(2, LexType.OF))
        self.stack.append(StackNode(2, LexType.RMIDPAREN))
        self.stack.append(StackNode(1, NontmlType.Top))
        self.stack.append(StackNode(2, LexType.UNDERANGE))
        self.stack.append(StackNode(1, NontmlType.Low))
        self.stack.append(StackNode(2, LexType.LMIDPAREN))
        self.stack.append(StackNode(2, LexType.ARRAY))

        self.currentP.kind["dec"] = DecKind.ArrayK
        # self.currentP.attr["ArrayAttr"]["childtype"] = self.temp
        self.tempp = (self.currentP, 2)

    def process20(self):
        self.stack.append(StackNode(2, LexType.INTC))
        self.currentP.attr["ArrayAttr"]["low"] = int(self.currentToken.Sem)
        self.currentP.linePos = self.currentToken.lineshow
        self.currentP.colPos = self.currentToken.col

    def process21(self):
        self.stack.append(StackNode(2, LexType.INTC))
        self.currentP.attr["ArrayAttr"]["up"] = int(self.currentToken.Sem)
        self.currentP.linePos = self.currentToken.lineshow
        self.currentP.colPos = self.currentToken.col

    def process22(self):
        self.stack.append(StackNode(2, LexType.END))
        self.stack.append(StackNode(1, NontmlType.FieldDecList))
        self.stack.append(StackNode(2, LexType.RECORD))

        self.currentP.kind["dec"] = DecKind.RecordK

        self.saveP = self.currentP

        self.stack_node.append((self.currentP, 0))

    def process23(self):
        self.stack.append(StackNode(1, NontmlType.FieldDecMore))
        self.stack.append(StackNode(2, LexType.SEMI))
        self.stack.append(StackNode(1, NontmlType.IdList))
        self.stack.append(StackNode(1, NontmlType.BaseType))

        self.currentP = newDecNode()
        # self.currentP.kind["dec"] = self.temp
        self.tempp = (self.currentP, 1)
        self.popNode(self.currentP)

        self.stack_node.append((self.currentP, -1))

    def process24(self):
        self.stack.append(StackNode(1, NontmlType.FieldDecMore))
        self.stack.append(StackNode(2, LexType.SEMI))
        self.stack.append(StackNode(1, NontmlType.IdList))
        self.stack.append(StackNode(1, NontmlType.ArrayType))

        self.currentP = newDecNode()
        self.popNode(self.currentP)

        self.stack_node.append((self.currentP, -1))

    def process25(self):
        self.popNode()
        self.currentP = self.saveP

    def process26(self):
        self.stack.append(StackNode(1, NontmlType.FieldDecList))

    def process27(self):
        self.stack.append(StackNode(1, NontmlType.IdMore))
        self.stack.append(StackNode(2, LexType.ID))

        self.currentP.name[self.currentP.idnum] = self.currentToken.Sem
        self.currentP.linePos = self.currentToken.lineshow
        self.currentP.colPos = self.currentToken.col
        self.currentP.idnum += 1

    def process28(self):
        pass

    def process29(self):
        self.stack.append(StackNode(1, NontmlType.IdList))
        self.stack.append(StackNode(2, LexType.COMMA))

    def process30(self):
        pass

    def process31(self):
        self.stack.append(StackNode(1, NontmlType.VarDeclaration))

    def process32(self):
        self.stack.append(StackNode(1, NontmlType.VarDecList))
        self.stack.append(StackNode(2, LexType.VAR))

        self.currentP = newVarNode()
        self.popNode(self.currentP)

        self.stack_node.append((self.currentP, -1))
        self.stack_node.append((self.currentP, 0))

    def process33(self):
        self.stack.append(StackNode(1, NontmlType.VarDecMore))
        self.stack.append(StackNode(2, LexType.SEMI))
        self.stack.append(StackNode(1, NontmlType.VarIdList))
        self.stack.append(StackNode(1, NontmlType.TypeName))

        self.currentP = newDecNode()
        self.popNode(self.currentP)

        self.stack_node.append((self.currentP, -1))

    def process34(self):
        self.popNode()

    def process35(self):
        self.stack.append(StackNode(1, NontmlType.VarDecList))

    def process36(self):
        self.stack.append(StackNode(1, NontmlType.VarIdMore))
        self.stack.append(StackNode(2, LexType.ID))
        self.currentP.name[self.currentP.idnum] = self.currentToken.Sem
        self.currentP.linePos = self.currentToken.lineshow
        self.currentP.colPos = self.currentToken.col
        self.currentP.idnum += 1

    def process37(self):
        pass

    def process38(self):
        self.stack.append(StackNode(1, NontmlType.VarIdList))
        self.stack.append(StackNode(2, LexType.COMMA))

    def process39(self):
        pass

    def process40(self):
        self.stack.append(StackNode(1, NontmlType.ProcDeclaration))

    def process41(self):
        self.stack.append(StackNode(1, NontmlType.ProcDecMore))
        self.stack.append(StackNode(1, NontmlType.ProcBody))
        self.stack.append(StackNode(1, NontmlType.ProcDecPart))
        self.stack.append(StackNode(2, LexType.SEMI))
        self.stack.append(StackNode(2, LexType.RPAREN))
        self.stack.append(StackNode(1, NontmlType.ParamList))
        self.stack.append(StackNode(2, LexType.LPAREN))
        self.stack.append(StackNode(1, NontmlType.ProcName))
        self.stack.append(StackNode(2, LexType.PROCEDURE))

        self.currentP = newProcNode()
        self.popNode(self.currentP)

        self.stack_node.append((self.currentP, -1))
        self.stack_node.append((self.currentP, 2))
        self.stack_node.append((self.currentP, 1))
        self.stack_node.append((self.currentP, 0))

    def process42(self):
        # 弹出过程节点的兄弟节点指针
        # popPA()
        # self.stack_node.pop()
        pass

    def process43(self):
        self.stack.append(StackNode(1, NontmlType.ProcDeclaration))

    def process44(self):
        self.stack.append(StackNode(2, LexType.ID))

        self.currentP.name[0] = self.currentToken.Sem
        self.currentP.linePos = self.currentToken.lineshow
        self.currentP.colPos = self.currentToken.col
        self.currentP.idnum += 1

    def process45(self):
        self.popNode()

    def process46(self):
        self.stack.append(StackNode(1, NontmlType.ParamDecList))

    def process47(self):
            self.stack.append(StackNode(1, NontmlType.ParamMore))
            self.stack.append(StackNode(1, NontmlType.Param))

    def process48(self):
        self.popNode()

    def process49(self):
        self.stack.append(StackNode(1, NontmlType.ParamDecList))
        self.stack.append(StackNode(2, LexType.SEMI))

    def process50(self):
        self.stack.append(StackNode(1, NontmlType.FormList))
        self.stack.append(StackNode(1, NontmlType.TypeName))

        self.currentP = newDecNode()
        self.currentP.attr["ProcAttr"]["paramt"] = ParamType.valparamType

        self.popNode(self.currentP)

        self.stack_node.append((self.currentP, -1))

    def process51(self):
        self.stack.append(StackNode(1, NontmlType.FormList))
        self.stack.append(StackNode(1, NontmlType.TypeName))
        self.stack.append(StackNode(2, LexType.VAR))

        self.currentP = newDecNode()
        self.currentP.attr["ProcAttr"]["paramt"] = ParamType.varparamType

        self.popNode(self.currentP)

        self.stack_node.append((self.currentP, -1))

    def process52(self):
        self.stack.append(StackNode(1, NontmlType.FidMore))
        self.stack.append(StackNode(2, LexType.ID))

        self.currentP.name[self.currentP.idnum] = self.currentToken.Sem
        self.currentP.linePos = self.currentToken.lineshow
        self.currentP.colPos = self.currentToken.col
        self.currentP.idnum += 1

    def process53(self):
        pass

    def process54(self):
        self.stack.append(StackNode(1, NontmlType.FormList))
        self.stack.append(StackNode(2, LexType.COMMA))

    def process55(self):
        self.stack.append(StackNode(1, NontmlType.DeclarePart))

    def process56(self):
        self.stack.append(StackNode(1, NontmlType.ProgramBody))

    def process57(self):
        self.stack.append(StackNode(2, LexType.END))
        self.stack.append(StackNode(1, NontmlType.StmList))
        self.stack.append(StackNode(2, LexType.BEGIN))

        self.popNode()

        self.currentP = newStmlNode()
        self.popNode(self.currentP)

        self.stack_node.append((self.currentP, 0))

    def process58(self):
        self.stack.append(StackNode(1, NontmlType.StmMore))
        self.stack.append(StackNode(1, NontmlType.Stm))

    def process59(self):
        self.popNode()

    def process60(self):
        self.stack.append(StackNode(1, NontmlType.StmList))
        self.stack.append(StackNode(2, LexType.SEMI))

    def process61(self):
        self.stack.append(StackNode(1, NontmlType.ConditionalStm))
        self.currentP = newStmtNode(StmtKind.IfK)

        self.popNode(self.currentP)
        self.stack_node.append((self.currentP, -1))

    def process62(self):
        self.stack.append(StackNode(1, NontmlType.LoopStm))
        self.currentP = newStmtNode(StmtKind.WhileK)

        self.popNode(self.currentP)
        self.stack_node.append((self.currentP, -1))

    def process63(self):
        self.stack.append(StackNode(1, NontmlType.InputStm))
        self.currentP = newStmtNode(StmtKind.ReadK)

        self.popNode(self.currentP)
        self.stack_node.append((self.currentP, -1))

    def process64(self):
        self.stack.append(StackNode(1, NontmlType.OutputStm))
        self.currentP = newStmtNode(StmtKind.WriteK)
        self.currentP.linePos = self.currentToken.lineshow
        self.currentP.colPos = self.currentToken.col

        self.popNode(self.currentP)
        self.stack_node.append((self.currentP, -1))

    def process65(self):
        self.stack.append(StackNode(1, NontmlType.ReturnStm))
        self.currentP = newStmtNode(StmtKind.ReturnK)
        self.currentP.linePos = self.currentToken.lineshow
        self.currentP.colPos = self.currentToken.col

        self.popNode(self.currentP)
        self.stack_node.append((self.currentP, -1))

    def process66(self):
        self.stack.append(StackNode(1, NontmlType.AssCall))
        self.stack.append(StackNode(2, LexType.ID))

        self.currentP = newStmtNode(StmtKind.AssignK)

        t1 = newExpNode(ExpKind.VariK)
        t1.name[0] = self.currentToken.Sem
        t1.linePos = self.currentToken.lineshow
        t1.colPos = self.currentToken.col
        t1.idnum += 1

        self.currentP.child[0] = t1

        self.popNode(self.currentP)
        #self.stack_node.append((self.currentP, -1))
        self.stack_node.append((self.currentP, -1))

    def process67(self):
        self.stack.append(StackNode(1, NontmlType.AssignmentRest))
        self.currentP.kind["stmt"] = StmtKind.AssignK

    def process68(self):
        self.stack.append(StackNode(1, NontmlType.CallStmRest))
        self.currentP.child[0].attr["ExpAttr"]["varkind"] = VarKind.IdV
        self.currentP.kind["stmt"] = StmtKind.CallK


    def process69(self):
        self.stack.append(StackNode(1, NontmlType.Exp))
        self.stack.append(StackNode(2, LexType.ASSIGN))
        self.stack.append(StackNode(1, NontmlType.VariMore))

        self.stack_node.append((self.currentP, 1))
        self.currentP = self.currentP.child[0]

        t = newExpNode(ExpKind.OpK)
        t.attr["ExpAttr"]["op"] = LexType.END
        self.stack_op.append(t)

    def process70(self):
        self.stack.append(StackNode(2, LexType.FI))
        self.stack.append(StackNode(1, NontmlType.StmList))
        self.stack.append(StackNode(2, LexType.ELSE))
        self.stack.append(StackNode(1, NontmlType.StmList))
        self.stack.append(StackNode(2, LexType.THEN))
        self.stack.append(StackNode(1, NontmlType.RelExp))
        self.stack.append(StackNode(2, LexType.IF))

        self.stack_node.append((self.currentP, 2))
        self.stack_node.append((self.currentP, 1))
        self.stack_node.append((self.currentP, 0))

    def process71(self):
        self.stack.append(StackNode(2, LexType.ENDWH))
        self.stack.append(StackNode(1, NontmlType.StmList))
        self.stack.append(StackNode(2, LexType.DO))
        self.stack.append(StackNode(1, NontmlType.RelExp))
        self.stack.append(StackNode(2, LexType.WHILE))

        self.stack_node.append((self.currentP, 1))
        self.stack_node.append((self.currentP, 0))

    def process72(self):
        self.stack.append(StackNode(2, LexType.RPAREN))
        self.stack.append(StackNode(1, NontmlType.InVar))
        self.stack.append(StackNode(2, LexType.LPAREN))
        self.stack.append(StackNode(2, LexType.READ))

    def process73(self):
        self.stack.append(StackNode(2, LexType.ID))
        self.currentP.name[0] = self.currentToken.Sem
        self.currentP.linePos = self.currentToken.lineshow
        self.currentP.colPos = self.currentToken.col
        self.currentP.idnum += 1

    def process74(self):
        self.stack.append(StackNode(2, LexType.RPAREN))
        self.stack.append(StackNode(1, NontmlType.Exp))
        self.stack.append(StackNode(2, LexType.LPAREN))
        self.stack.append(StackNode(2, LexType.WRITE))

        self.stack_node.append((self.currentP, 0))

        t = newExpNode(ExpKind.OpK)
        t.attr["ExpAttr"]["op"] = LexType.END
        self.stack_op.append(t)

    def process75(self):
        self.stack.append(StackNode(2, LexType.RETURN))

    def process76(self):
        self.stack.append(StackNode(2, LexType.RPAREN))
        self.stack.append(StackNode(1, NontmlType.ActParamList))
        self.stack.append(StackNode(2, LexType.LPAREN))

        self.stack_node.append((self.currentP, 1))

    def process77(self):
        self.popNode()

    def process78(self):
        self.stack.append(StackNode(1, NontmlType.ActParamMore))
        self.stack.append(StackNode(1, NontmlType.Exp))

        t = newExpNode(ExpKind.OpK)
        t.attr["ExpAttr"]["op"] = LexType.END
        self.stack_op.append(t)

    def process79(self):
        pass

    def process80(self):
        self.stack.append(StackNode(1, NontmlType.ActParamList))
        self.stack.append(StackNode(2, LexType.COMMA))

        self.stack_node.append((self.currentP, -1))

    def process81(self):
        self.stack.append(StackNode(1, NontmlType.OtherRelE))
        self.stack.append(StackNode(1, NontmlType.Exp))

        t = newExpNode(ExpKind.OpK)
        t.attr["ExpAttr"]["op"] = LexType.END

        self.stack_op.append(t)
        self.getExpResult = False

    def process82(self):
        self.stack.append(StackNode(1, NontmlType.Exp))
        self.stack.append(StackNode(1, NontmlType.CmpOp))

        self.currentP = newExpNode(ExpKind.OpK)
        self.currentP.attr["ExpAttr"]["op"] = self.currentToken.Lex
        self.currentP.linePos = self.currentToken.lineshow
        self.currentP.colPos = self.currentToken.col

        sTop = self.stack_op[-1].attr["ExpAttr"]["op"]
        while self.Priosity(sTop) >= self.Priosity(self.currentToken.Lex):
            t = self.stack_op.pop()
            Rnum = self.stack_num.pop()
            Lnum = self.stack_num.pop()
            t.child[0] = Lnum
            t.child[1] = Rnum
            self.stack_num.append(t)
            sTop = self.stack_op[-1].attr["ExpAttr"]["op"]
        self.stack_op.append(self.currentP)
        self.getExpResult = True

    def process83(self):
        self.stack.append(StackNode(1, NontmlType.OtherTerm))
        self.stack.append(StackNode(1, NontmlType.Term))

    def process84(self):
        if self.currentToken.Lex == LexType.RPAREN and self.expflag != 0:
            while self.stack_op[-1].attr["ExpAttr"]["op"] != LexType.LPAREN:
                t = self.stack_op.pop()
                Rnum = self.stack_num.pop()
                Lnum = self.stack_num.pop()
                t.child[0] = Lnum
                t.child[1] = Rnum
                self.stack_num.append(t)
            self.stack_op.pop()
            self.expflag -= 1
        else:
            if self.getExpResult is True or self.getExpResult2 is True:
                while self.stack_op[-1].attr["ExpAttr"]["op"] != LexType.END:
                    t = self.stack_op.pop()
                    Rnum = self.stack_num.pop()
                    Lnum = self.stack_num.pop()
                    t.child[0] = Lnum
                    t.child[1] = Rnum
                    self.stack_num.append(t)
                self.stack_op.pop()
                self.currentP = self.stack_num.pop()
                self.popNode(self.currentP)
                if self.getExpResult2 is True:
                    self.getExpResult2 = False

    def process85(self):
        self.stack.append(StackNode(1, NontmlType.Exp))
        self.stack.append(StackNode(1, NontmlType.AddOp))

        self.currentP = newExpNode(ExpKind.OpK)
        self.currentP.attr["ExpAttr"]["op"] = self.currentToken.Lex
        self.currentP.linePos = self.currentToken.lineshow
        self.currentP.colPos = self.currentToken.col

        sTop = self.stack_op[-1].attr["ExpAttr"]["op"]
        while self.Priosity(sTop) >= self.Priosity(self.currentToken.Lex):
            t = self.stack_op.pop()
            Rnum = self.stack_num.pop()
            Lnum = self.stack_num.pop()
            t.child[0] = Lnum
            t.child[1] = Rnum
            self.stack_num.append(t)
            sTop = self.stack_op[-1].attr["ExpAttr"]["op"]
        self.stack_op.append(self.currentP)

    def process86(self):
        self.stack.append(StackNode(1, NontmlType.OtherFactor))
        self.stack.append(StackNode(1, NontmlType.Factor))

    def process87(self):
        pass

    def process88(self):
        self.stack.append(StackNode(1, NontmlType.Term))
        self.stack.append(StackNode(1, NontmlType.MultOp))

        self.currentP = newExpNode(ExpKind.OpK)
        self.currentP.attr["ExpAttr"]["op"] = self.currentToken.Lex
        self.currentP.linePos = self.currentToken.lineshow
        self.currentP.colPos = self.currentToken.col

        sTop = self.stack_op[-1].attr["ExpAttr"]["op"]
        while self.Priosity(sTop) >= self.Priosity(self.currentToken.Lex):
            t = self.stack_op.pop()
            Rnum = self.stack_num.pop()
            Lnum = self.stack_num.pop()
            t.child[0] = Lnum
            t.child[1] = Rnum
            self.stack_num.append(t)
            sTop = self.stack_op[-1].attr["ExpAttr"]["op"]
        self.stack_op.append(self.currentP)

    def process89(self):
        self.stack.append(StackNode(2, LexType.RPAREN))
        self.stack.append(StackNode(1, NontmlType.Exp))
        self.stack.append(StackNode(2, LexType.LPAREN))

        t = newExpNode(ExpKind.OpK)
        t.attr["ExpAttr"]["op"] = self.currentToken.Lex
        self.currentP.linePos = self.currentToken.lineshow
        self.currentP.colPos = self.currentToken.col
        self.stack_op.append(t)
        self.expflag += 1

    def process90(self):
        self.stack.append(StackNode(2, LexType.INTC))

        t = newExpNode(ExpKind.ConstK)
        t.attr["ExpAttr"]["val"] = int(self.currentToken.Sem)
        t.linePos = self.currentToken.lineshow
        t.colPos = self.currentToken.col
        self.stack_num.append(t)

    def process91(self):
        self.stack.append(StackNode(1, NontmlType.Variable))

    def process92(self):
        self.stack.append(StackNode(1, NontmlType.VariMore))
        self.stack.append(StackNode(2, LexType.ID))

        self.currentP = newExpNode(ExpKind.VariK)
        self.currentP.name[0] = self.currentToken.Sem
        self.currentP.linePos = self.currentToken.lineshow
        self.currentP.colPos = self.currentToken.col
        self.currentP.idnum += 1

        self.stack_num.append(self.currentP)

    def process93(self):
        self.currentP.attr["ExpAttr"]["varkind"] = VarKind.IdV

    def process94(self):
        self.stack.append(StackNode(2, LexType.RMIDPAREN))
        self.stack.append(StackNode(1, NontmlType.Exp))
        self.stack.append(StackNode(2, LexType.LMIDPAREN))

        self.currentP.attr["ExpAttr"]["varkind"] = VarKind.ArrayMembV
        self.stack_node.append((self.currentP, 0))

        t = newExpNode(ExpKind.OpK)
        t.attr["ExpAttr"]["op"] = LexType.END
        self.stack_op.append(t)

        self.getExpResult2 = True

    def process95(self):
        self.stack.append(StackNode(1, NontmlType.FieldVar))
        self.stack.append(StackNode(2, LexType.DOT))

        self.currentP.attr["ExpAttr"]["varkind"] = VarKind.FieldMembV
        self.stack_node.append((self.currentP, 0))

    def process96(self):
        self.stack.append(StackNode(1, NontmlType.FieldVarMore))
        self.stack.append(StackNode(2, LexType.ID))

        self.currentP = newExpNode(ExpKind.VariK)
        self.currentP.name[0] = self.currentToken.Sem
        self.currentP.linePos = self.currentToken.lineshow
        self.currentP.colPos = self.currentToken.col
        self.currentP.idnum += 1
        self.popNode(self.currentP)

    def process97(self):
        self.currentP.attr["ExpAttr"]["varkind"] = VarKind.IdV

    def process98(self):
        self.stack.append(StackNode(2, LexType.RMIDPAREN))
        self.stack.append(StackNode(1, NontmlType.Exp))
        self.stack.append(StackNode(2, LexType.LMIDPAREN))

        self.currentP.attr["ExpAttr"]["varkind"] = VarKind.ArrayMembV
        self.stack_node.append((self.currentP, 0))

        t = newExpNode(ExpKind.OpK)
        t.attr["ExpAttr"]["op"] = LexType.END
        self.stack_op.append(t)

        self.getExpResult2 = True

    def process99(self):
        self.stack.append(StackNode(2, LexType.LT))

    def process100(self):
        self.stack.append(StackNode(2, LexType.EQ))

    def process101(self):
        self.stack.append(StackNode(2, LexType.PLUS))

    def process102(self):
        self.stack.append(StackNode(2, LexType.MINUS))

    def process103(self):
        self.stack.append(StackNode(2, LexType.TIMES))

    def process104(self):
        self.stack.append(StackNode(2, LexType.OVER))

    def predict(self, num):
        if 1 <= num <= 104:
            eval("self.process" + str(num))()
        else:
            self.error.append(
                "in line:{0} col{1}, {2} wrong".format(self.currentToken.linePos, self.currentToken.colPos,
                                                       self.currentToken.Sem))

    def printstack(self):
        for t in self.stack:
            if t.Ntmlvar is None:
                print(t.tmlvar, end=' ')
            else:
                print(t.Ntmlvar, end=' ')
        print()
        for t, v in self.stack_node:
            print("node", t.nodeKind, v)
        for t in self.stack_op:
            print("op", t.nodeKind, t.attr)
        for t in self.stack_num:
            print("num", t.nodeKind, t.attr)

    def parse(self, tokens):
        table = LL1Table()
        self.tokens = tokens
        root = newRootNode()
        self.currentP = root
        self.stack_node.append((root, 2))
        self.stack_node.append((root, 1))
        self.stack_node.append((root, 0))

        self.stack.append(StackNode(1, NontmlType.Program))

        self.currentToken = self.gettoken()
        lineno = self.currentToken.lineshow

        wrong_Flag = False
        while len(self.stack) != 0 and wrong_Flag is False:
            toptoken = self.stack[-1]
            #if self.currentToken.lineshow == 32:
            # print(pnum, self.currentToken.Lex, '|||', end=' ')
            # self.printstack()

            if toptoken.flag == 2:
                self.stacktopT = toptoken.tmlvar

                if self.stacktopT == self.currentToken.Lex:
                    self.stack.pop()
                    self.currentToken = self.gettoken()
                else:
                    self.error.append("in line:{0} col{1}, {2} wrong".format(self.currentToken.linePos, self.currentToken.colPos, self.currentToken.Sem))
            else:
                self.stacktopN = toptoken.Ntmlvar
                pnum = table.getPredict(self.stacktopN, self.currentToken.Lex)
                self.stack.pop()
                self.predict(pnum)

        return root


if __name__ == '__main__':
    programPath = sys.argv[1]   #程序产物文件夹
    input_path = programPath + '/tk'
    output_path = programPath + '/treell1'
    error_path = programPath + '/treell1err'

    # input_path = "../../../outputs/test_demos/bubble_sort.tk"
    # output_path = None
    # input_path = "input1.txt"
    # input_path = "../../../outputs/test_demos/test_output_tokens2.txt"
    # output_path = "out2.txt"
    # output_path = "bubble.out"
    # input_path = "../outputs/bubble_sort.tk"

    with open(input_path, 'r') as f:
        input_file = json.load(f)

    LL1 = LL1Parse()
    root = LL1.parse(input_file)
    IOClass = IONode()
    IOClass.printRoot(root, file=output_path)
    if len(LL1.error) != 0:
        with open(error_path, 'w') as f:
            print(LL1.error, file=f)
    #IOClass.printRoot(root)
    # rr = IOClass.loadroot("tmp.txt")
    # IOClass.printRoot(rr)

