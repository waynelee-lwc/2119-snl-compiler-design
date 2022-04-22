from src.semantic_analysis.SemanticSupport import *

LOG = Log()
TAG = "symbTbale.py"
DEBUG = "sym.py"
str1 = "ab2c"
str2 = "abc"


class ParamTable:
    def __init__(self):
        entry = Symbtable()
        next = None


class Symbtable:
    def __init__(self):
        self.idName = ""
        self.attrIR = AttributeIR()
        self.next = None


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

def ErrorPrompt(self, line, name, message):
    LOG.e(TAG, ">>>Line: {} {} {}".format(str(line), name, message))
    Error = True
    exit(-1)

initOff = 7