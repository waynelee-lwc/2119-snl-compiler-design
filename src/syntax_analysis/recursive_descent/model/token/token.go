package token

//Token
type TokenType string

const (
	Number     TokenType = "NUMBER"
	ID         TokenType = "ID"
	Assign     TokenType = "ASSIGN"
	Seperator  TokenType = "SEPERATOR"
	EOF        TokenType = "EOF"
	UnderRange TokenType = "UNDERANGE"
	Char       TokenType = "CHARc"
	Reserved   TokenType = "RESERVED"
)

var noNeedToCmpName = map[TokenType]interface{}{
	Number:     true,
	Assign:     true,
	EOF:        true,
	Char:       true,
	ID:         true,
	UnderRange: true,
}

type Token struct {
	Type   TokenType `json:"type"`
	Name   string    `json:"name"`
	Line   int       `json:"line"`
	Column int       `json:"col"`
}

func NewToken(type_ TokenType, name string, line int, column int) *Token {
	return &Token{
		Type:   type_,
		Name:   name,
		Line:   line,
		Column: column,
	}
}

//token坚定，部分token不需要比较具体内容
func (t Token) Compare(token *Token) bool {
	if token == nil {
		return false
	}
	if t.Type != token.Type {
		return false
	}
	if _, ok := noNeedToCmpName[token.Type]; ok {
		return true
	}
	return t.Name == token.Name
}

var (
	GeneralizedID     = NewToken(ID, "", 0, 0)
	GeneralizedNumber = NewToken(Number, "", 0, 0)
	GeneralizedCharc  = NewToken(Char, "", 0, 0)
	TokenAssign       = NewToken(Assign, ":=", 0, 0)
	TokenEof          = NewToken(EOF, "EOF", 0, 0)
	TokenUnderRange   = NewToken(UnderRange, "", 0, 0)

	ReservedProgram   = NewToken(Reserved, "program", 0, 0)
	ReservedProcedure = NewToken(Reserved, "procedure", 0, 0)
	ReservedType      = NewToken(Reserved, "type", 0, 0)
	ReservedVar       = NewToken(Reserved, "var", 0, 0)
	ReservedIf        = NewToken(Reserved, "if", 0, 0)
	ReservedThen      = NewToken(Reserved, "then", 0, 0)
	ReservedElse      = NewToken(Reserved, "else", 0, 0)
	ReservedFi        = NewToken(Reserved, "fi", 0, 0)
	ReservedWhile     = NewToken(Reserved, "while", 0, 0)
	ReservedDo        = NewToken(Reserved, "do", 0, 0)
	ReservedEndWhile  = NewToken(Reserved, "endwh", 0, 0)
	ReservedBegin     = NewToken(Reserved, "begin", 0, 0)
	ReservedEnd       = NewToken(Reserved, "end", 0, 0)
	ReservedRead      = NewToken(Reserved, "read", 0, 0)
	ReservedWrite     = NewToken(Reserved, "write", 0, 0)
	ReservedArray     = NewToken(Reserved, "array", 0, 0)
	ReservedOf        = NewToken(Reserved, "of", 0, 0)
	ReservedRecord    = NewToken(Reserved, "record", 0, 0)
	ReservedReturn    = NewToken(Reserved, "return", 0, 0)
	ReservedInteger   = NewToken(Reserved, "integer", 0, 0)

	SeperatorPlus      = NewToken(Seperator, "+", 0, 0)
	SeperatorMinus     = NewToken(Seperator, "-", 0, 0)
	SeperatorTimes     = NewToken(Seperator, "*", 0, 0)
	SeperatorOver      = NewToken(Seperator, "/", 0, 0)
	SeperatorLParen    = NewToken(Seperator, "(", 0, 0)
	SeperatorRParen    = NewToken(Seperator, ")", 0, 0)
	SeperatorDot       = NewToken(Seperator, ".", 0, 0)
	SeperatorColon     = NewToken(Seperator, ":", 0, 0)
	SeperatorSemi      = NewToken(Seperator, ";", 0, 0)
	SeperatorComma     = NewToken(Seperator, ",", 0, 0)
	SeperatorLMidParen = NewToken(Seperator, "[", 0, 0)
	SeperatorRMidParen = NewToken(Seperator, "]", 0, 0)
	SeperatorLT        = NewToken(Seperator, "<", 0, 0)
	SeperatorEqual     = NewToken(Seperator, "=", 0, 0)
)
