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

func VarIdList(node *tree_node.TreeNode) error {

	if id, err := Match(token_set.ID); err != nil {
		return fmt.Errorf("VarIdList parse failed! %v", err)
	} else {
		node.Name = append(node.Name, id.Name)
		node.IdNum++
	}
	if err := VarIdMore(node); err != nil {
		return fmt.Errorf("VarIdList parse failed! %v", err)
	}

	return nil
}

func VarIdMore(node *tree_node.TreeNode) error {
	currToken, _ := token_set.Scanner.GetCurr()

	if token_set.VarIdMore2Nil.Predict(currToken) {
		return nil
	}
	if token_set.VarIdMore2VarIdList.Predict(currToken) {
		if _, err := Match(token_set.Comma); err != nil {
			return fmt.Errorf("VarIdMore parse failed! %v", err)
		}
		if err := VarIdList(node); err != nil {
			return fmt.Errorf("VarIdMore parse failed! %v", err)
		}
		return nil
	}

	return fmt.Errorf("VarIdMore match failed! %v", currToken)
}

func FormList(node *tree_node.TreeNode) error {
	if id, err := Match(token_set.ID); err != nil {
		return fmt.Errorf("FormList parse failed! %v", err)
	} else {
		node.Name = append(node.Name, id.Name)
	}
	if err := FidMore(node); err != nil {
		return fmt.Errorf("FormList parse failed! %v", err)
	}

	return nil
}

func FidMore(node *tree_node.TreeNode) error {
	currToken, _ := token_set.Scanner.GetCurr()

	if token_set.FidMore2Nil.Predict(currToken) {
		return nil
	}
	if token_set.FidMore2FormList.Predict(currToken) {
		if _, err := Match(token_set.Comma); err != nil {
			return fmt.Errorf("FidMore parse failed! %v", err)
		}
		if err := FormList(node); err != nil {
			return fmt.Errorf("FidMore parse failed! %v", err)
		}
	}

	return nil
}
