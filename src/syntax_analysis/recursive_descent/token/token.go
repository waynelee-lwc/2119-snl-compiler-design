package token

import "recursive_descent_parser/model"

const (
	ID         model.TokenType = "ID"
	Reserved   model.TokenType = "RESERVED"
	Number     model.TokenType = "NUMBER"
	Charc      model.TokenType = "CHARC"
	Seperator  model.TokenType = "SEPERATOR"
	Assign     model.TokenType = "ASSIGN"
	Eof        model.TokenType = "EOF"
	UnderRange model.TokenType = "UNDERANGE"
)

var (
	GeneralizedID     = model.NewToken(ID, "", 0, 0)
	GeneralizedNumber = model.NewToken(Number, "", 0, 0)
	GeneralizedCharc  = model.NewToken(Charc, "", 0, 0)
	TokenAssign       = model.NewToken(Assign, ":=", 0, 0)
	TokenEof          = model.NewToken(Eof, "EOF", 0, 0)
	TokenUnderRange   = model.NewToken(UnderRange, "", 0, 0)

	ReservedProgram   = model.NewToken(Reserved, "program", 0, 0)
	ReservedProcedure = model.NewToken(Reserved, "procedure", 0, 0)
	ReservedType      = model.NewToken(Reserved, "type", 0, 0)
	ReservedVar       = model.NewToken(Reserved, "var", 0, 0)
	ReservedIf        = model.NewToken(Reserved, "if", 0, 0)
	ReservedThen      = model.NewToken(Reserved, "then", 0, 0)
	ReservedElse      = model.NewToken(Reserved, "else", 0, 0)
	ReservedFi        = model.NewToken(Reserved, "fi", 0, 0)
	ReservedWhile     = model.NewToken(Reserved, "while", 0, 0)
	ReservedDo        = model.NewToken(Reserved, "do", 0, 0)
	ReservedEndWhile  = model.NewToken(Reserved, "endwh", 0, 0)
	ReservedBegin     = model.NewToken(Reserved, "begin", 0, 0)
	ReservedEnd       = model.NewToken(Reserved, "end", 0, 0)
	ReservedRead      = model.NewToken(Reserved, "read", 0, 0)
	ReservedWrite     = model.NewToken(Reserved, "write", 0, 0)
	ReservedArray     = model.NewToken(Reserved, "array", 0, 0)
	ReservedOf        = model.NewToken(Reserved, "of", 0, 0)
	ReservedRecord    = model.NewToken(Reserved, "record", 0, 0)
	ReservedReturn    = model.NewToken(Reserved, "return", 0, 0)
	ReservedInteger   = model.NewToken(Reserved, "integer", 0, 0)
	TableOfReserved   = map[string]model.Token{}

	// SeperatorPlus 	  = model.NewToken(Seperator, "", 0, 0)
	// SeperatorPlus 	  = model.NewToken(Seperator, "", 0, 0)
	// SeperatorPlus 	  = model.NewToken(Seperator, "", 0, 0)
	// SeperatorPlus 	  = model.NewToken(Seperator, "", 0, 0)
	// SeperatorPlus 	  = model.NewToken(Seperator, "", 0, 0)
	// SeperatorPlus 	  = model.NewToken(Seperator, "", 0, 0)
	// SeperatorPlus 	  = model.NewToken(Seperator, "", 0, 0)
	// SeperatorPlus 	  = model.NewToken(Seperator, "", 0, 0)
)
