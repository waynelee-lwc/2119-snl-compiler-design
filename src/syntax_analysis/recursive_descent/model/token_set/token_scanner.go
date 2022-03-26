package token_set

import (
	"fmt"
	"recursive_descent_parser/model/token"
)

type TokenScanner struct {
	tokenList []*token.Token
	len       int
	idx       int
}

func (scanner *TokenScanner) Reset() {
	scanner.idx = 0
}

func (scanner *TokenScanner) Length() int {
	return scanner.len
}

func (scanner *TokenScanner) HasNext() bool {
	return scanner.idx < scanner.len
}

func (scanner *TokenScanner) GetCurr() (*token.Token, error) {
	if !scanner.HasNext() {
		return nil, fmt.Errorf("no more tokens!%v/%v", scanner.idx, scanner.len)
	}
	return scanner.tokenList[scanner.idx], nil
}

func (scanner *TokenScanner) Next() error {
	if !scanner.HasNext() {
		return fmt.Errorf("no more tokens!%v/%v", scanner.idx, scanner.len)
	}
	scanner.idx++
	return nil
}

func (scanner *TokenScanner) Poll() (*token.Token, error) {
	if !scanner.HasNext() {
		return nil, fmt.Errorf("no more tokens!%v/%v", scanner.idx, scanner.len)
	}
	token := scanner.tokenList[scanner.idx]
	scanner.Next()
	return token, nil
}

var Scanner TokenScanner

func Initscanner(tokenList []*token.Token) {
	Scanner = TokenScanner{
		tokenList: tokenList,
		len:       len(tokenList),
		idx:       0,
	}
}
