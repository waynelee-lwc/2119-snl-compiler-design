package statement

import (
	"fmt"
	tokens "recursive_descent_parser/model/token"
	"recursive_descent_parser/model/token_set"
)

func Match(expected *tokens.Token) (*tokens.Token, error) {
	token, err := token_set.Scanner.Poll()
	if err != nil {
		return nil, err
	}
	if expected.Compare(token) {
		fmt.Println("match!", expected, token)
		return token, nil
	}
	return nil, fmt.Errorf("token not match! %v:%v", expected, token)
}
