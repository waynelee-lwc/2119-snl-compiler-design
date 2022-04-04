package statement

import (
	"fmt"
	"recursive_descent_parser/model/token_set"
	"recursive_descent_parser/model/tree_node"
)

func BaseType() (tree_node.Kind, error) {
	currToken, err := token_set.Scanner.GetCurr()
	if err != nil {
		return "", err
	}
	if token_set.BaseType2Integer.Predict(currToken) {
		if _, err := Match(token_set.Integer); err != nil {
			return "", fmt.Errorf("BaseType  %v", err)
		}
		return tree_node.IntegerK, nil
	}
	if token_set.BaseType2Char.Predict(currToken) {
		if _, err := Match(token_set.Char); err != nil {
			return "", fmt.Errorf("BaseType  %v", err)
		}
		return tree_node.CharK, nil
	}
	return "", fmt.Errorf("base type match error!%v", currToken)
}
