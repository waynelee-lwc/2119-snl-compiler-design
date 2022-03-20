package model

type TokenType string

type Token struct {
	Type   TokenType `json:"type"`
	Name   string    `json:"name"`
	Line   int       `json:"line"`
	Column int       `json:"col"`
}

func NewToken(type_ TokenType, name string, line int, column int) Token {
	return Token{
		Type:   type_,
		Name:   name,
		Line:   line,
		Column: column,
	}
}
