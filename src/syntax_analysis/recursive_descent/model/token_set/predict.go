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
)
