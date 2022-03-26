package statement

import (
	"fmt"
	"recursive_descent_parser/model/token_set"
	"recursive_descent_parser/model/tree_node"
)

func IdList(node *tree_node.TreeNode) error {
	if id, err := Match(token_set.ID); err != nil {
		return fmt.Errorf("IdList parse failed! %v", err)
	} else {
		node.Name = append(node.Name, id.Name)
	}

	return IdMore(node)
}

func IdMore(node *tree_node.TreeNode) error {
	currToken, _ := token_set.Scanner.GetCurr()

	if token_set.IdMore2Nil.Predict(currToken) {
		return nil
	}
	if token_set.IdMore2IdList.Predict(currToken) {
		if _, err := Match(token_set.Comma); err != nil {
			return fmt.Errorf("IdMore parse failed! %v", err)
		}
		return IdList(node)
	}

	return fmt.Errorf("IdMore match failed! %v", currToken)
}
