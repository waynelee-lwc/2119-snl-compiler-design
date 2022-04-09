package token_set

import "recursive_descent_parser/model/token"

var (
	ID     = token.NewToken(token.ID, "", 0, 0)
	Number = token.NewToken(token.Number, "", 0, 0)
	Charc  = token.NewToken(token.Char, "", 0, 0)
	Assign = token.NewToken(token.Assign, ":=", 0, 0)
	Eof    = token.NewToken(token.EOF, "EOF", 0, 0)
	Range  = token.NewToken(token.UnderRange, "", 0, 0)

	Program   = token.NewToken(token.Reserved, "program", 0, 0)
	Procedure = token.NewToken(token.Reserved, "procedure", 0, 0)
	Type      = token.NewToken(token.Reserved, "type", 0, 0)
	Var       = token.NewToken(token.Reserved, "var", 0, 0)
	If        = token.NewToken(token.Reserved, "if", 0, 0)
	Then      = token.NewToken(token.Reserved, "then", 0, 0)
	Else      = token.NewToken(token.Reserved, "else", 0, 0)
	Fi        = token.NewToken(token.Reserved, "fi", 0, 0)
	While     = token.NewToken(token.Reserved, "while", 0, 0)
	Do        = token.NewToken(token.Reserved, "do", 0, 0)
	EndWhile  = token.NewToken(token.Reserved, "endwh", 0, 0)
	Begin     = token.NewToken(token.Reserved, "begin", 0, 0)
	End       = token.NewToken(token.Reserved, "end", 0, 0)
	Read      = token.NewToken(token.Reserved, "read", 0, 0)
	Write     = token.NewToken(token.Reserved, "write", 0, 0)
	Array     = token.NewToken(token.Reserved, "array", 0, 0)
	Of        = token.NewToken(token.Reserved, "of", 0, 0)
	Record    = token.NewToken(token.Reserved, "record", 0, 0)
	Return    = token.NewToken(token.Reserved, "return", 0, 0)
	Integer   = token.NewToken(token.Reserved, "integer", 0, 0)
	Char      = token.NewToken(token.Reserved, "char", 0, 0)

	Plus      = token.NewToken(token.Seperator, "+", 0, 0)
	Minus     = token.NewToken(token.Seperator, "-", 0, 0)
	Times     = token.NewToken(token.Seperator, "*", 0, 0)
	Over      = token.NewToken(token.Seperator, "/", 0, 0)
	LParen    = token.NewToken(token.Seperator, "(", 0, 0)
	RParen    = token.NewToken(token.Seperator, ")", 0, 0)
	Dot       = token.NewToken(token.Seperator, ".", 0, 0)
	Colon     = token.NewToken(token.Seperator, ":", 0, 0)
	Semi      = token.NewToken(token.Seperator, ";", 0, 0)
	Comma     = token.NewToken(token.Seperator, ",", 0, 0)
	LMidParen = token.NewToken(token.Seperator, "[", 0, 0)
	RMidParen = token.NewToken(token.Seperator, "]", 0, 0)
	LT        = token.NewToken(token.Seperator, "<", 0, 0)
	Equal     = token.NewToken(token.Seperator, "=", 0, 0)
)

//Predict集合
type PredictSet []*token.Token

//判断给定token是否属于predict集合
func (p PredictSet) Predict(token *token.Token) bool {
	for _, t := range p {
		if t.Compare(token) {
			return true
		}
	}
	return false
}

var (
	DemoPredict = PredictSet{Program, Procedure, ID, Colon}

	//类型定义节点
	TypeDec2Nil             = PredictSet{Var, Procedure, Begin}
	TypeDec2TypeDeclaration = PredictSet{Type}

	TypeDecMore2Nil         = PredictSet{Var, Procedure, Begin}
	TypeDecMore2TypeDecList = PredictSet{ID}

	TypeDef2BaseType      = PredictSet{Integer, Char}
	TypeDef2StructureType = PredictSet{Array, Record}
	TypeDef2Id            = PredictSet{ID}

	BaseType2Integer = PredictSet{Integer}
	BaseType2Char    = PredictSet{Char}

	StructureType2ArrayType = PredictSet{Array}
	StructureTYpe2RecType   = PredictSet{Record}

	FieldDecList2BaseType  = PredictSet{Integer, Char}
	FieldDecList2ArrayType = PredictSet{Array}

	FieldDecMore2Nil          = PredictSet{End}
	FieldDecMore2FieldDecList = PredictSet{Integer, Char, Array}

	IdMore2Nil    = PredictSet{Semi}
	IdMore2IdList = PredictSet{Comma}

	VarDec2Nil            = PredictSet{Procedure, Begin}
	VarDec2VarDeclaration = PredictSet{Var}

	VarDecMore2Nil        = PredictSet{Procedure, Begin}
	VarDecMore2VarDecList = PredictSet{Integer, Char, Record, Array, ID}

	VarIdMore2Nil       = PredictSet{Semi}
	VarIdMore2VarIdList = PredictSet{Comma}

	ProcDec2Nil             = PredictSet{Begin}
	ProcDec2ProcDeclaration = PredictSet{Procedure}

	ProcDecMore2Nil     = PredictSet{Begin}
	ProcDecMore2ProcDec = PredictSet{Procedure}

	ParamList2Nil          = PredictSet{RParen}
	ParamList2ParamDecList = PredictSet{Integer, Char, Array, Record, ID, Var}

	ParamMore2Nil          = PredictSet{RParen}
	ParamMore2ParamDecList = PredictSet{Semi}

	ParamVal = PredictSet{Integer, Char, Record, Array, ID}
	ParamVar = PredictSet{Var}

	FidMore2Nil      = PredictSet{Semi, RParen}
	FidMore2FormList = PredictSet{Comma}

	StmMore2Nil     = PredictSet{End, EndWhile, Else, Fi} //分支情况要考虑！
	StmMore2StmList = PredictSet{Semi}

	Stm2ConditionalStm = PredictSet{If}
	Stm2LoopStm        = PredictSet{While}
	Stm2InputStm       = PredictSet{Read}
	Stm2OutputStm      = PredictSet{Write}
	Stm2ReturnStm      = PredictSet{Return}
	Stm2AssCal         = PredictSet{ID}

	AssCall2AssignmentRest = PredictSet{Assign, Dot, LMidParen} //这个要加一个Dot，和左中括号，考虑左值是记录或者数组！
	AssCall2CallStmRest    = PredictSet{LParen}

	ActParamList2Nil          = PredictSet{RParen}
	ActParamList2ActParamList = PredictSet{ID, Number}

	ActParamMore2Nil          = PredictSet{RParen}
	ActParamMore2ActParamList = PredictSet{Comma}

	OtherTerm2Nil   = PredictSet{LT, Equal, RMidParen, Then, Else, Fi, Do, EndWhile, RParen, End, Semi, Comma}
	OtherTerm2AddOp = PredictSet{Plus, Minus}

	CmpOp2EQ = PredictSet{Equal}
	CmpOp2LT = PredictSet{LT}

	AddOp2Plus  = PredictSet{Plus}
	AddOp2Minus = PredictSet{Minus}

	MultOp2Times = PredictSet{Times}
	MultOp2Over  = PredictSet{Over}

	Factor2Exp      = PredictSet{LParen}
	Factor2IntC     = PredictSet{Number}
	Factor2CharC    = PredictSet{Charc} //这里要添加单个字符的情况
	Factor2Variable = PredictSet{ID}

	OtherFactor2Nil    = PredictSet{Plus, Minus, LT, Equal, RMidParen, Then, Else, Fi, Do, EndWhile, RParen, End, Semi, Comma}
	OtherFactor2MultOp = PredictSet{Times, Over}

	VariMore2Nil      = PredictSet{Assign, Times, Over, Plus, Minus, LT, Equal, Then, Else, Fi, Do, EndWhile, RMidParen, RParen, End, Semi, Comma}
	VariMore2Exp      = PredictSet{LMidParen}
	VariMore2FieldVar = PredictSet{Dot}

	FieldVarMore2Nil = PredictSet{Assign, Times, Over, Plus, Minus, LT, Equal, Then, Else, Fi, Do, EndWhile, RMidParen, RParen, End, Semi, Comma}
	FieldVarMore2Exp = PredictSet{LMidParen}
)
