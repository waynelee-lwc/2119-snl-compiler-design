package statement

import (
	"fmt"
	"recursive_descent_parser/model/token_set"
	"recursive_descent_parser/model/tree_node"
)

func IdList(node *tree_node.TreeNode) error {
	if id, err := Match(token_set.ID); err != nil {
		return fmt.Errorf("IdList  %v", err)
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
			return fmt.Errorf("IdMore  %v", err)
		}
		return IdList(node)
	}

	return fmt.Errorf("IdMore match failed! %v", currToken)
}

func VarIdList(node *tree_node.TreeNode) error {

	if id, err := Match(token_set.ID); err != nil {
		return fmt.Errorf("VarIdList  %v", err)
	} else {
		node.Name = append(node.Name, id.Name)
		node.IdNum++
	}
	if err := VarIdMore(node); err != nil {
		return fmt.Errorf("VarIdList  %v", err)
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
			return fmt.Errorf("VarIdMore  %v", err)
		}
		if err := VarIdList(node); err != nil {
			return fmt.Errorf("VarIdMore  %v", err)
		}
		return nil
	}

	return fmt.Errorf("VarIdMore match failed! %v", currToken)
}

func FormList(node *tree_node.TreeNode) error {
	if id, err := Match(token_set.ID); err != nil {
		return fmt.Errorf("FormList  %v", err)
	} else {
		node.Name = append(node.Name, id.Name)
	}
	if err := FidMore(node); err != nil {
		return fmt.Errorf("FormList  %v", err)
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
			return fmt.Errorf("FidMore  %v", err)
		}
		if err := FormList(node); err != nil {
			return fmt.Errorf("FidMore  %v", err)
		}
	}

	return nil
}

func ActParamList() ([]*tree_node.TreeNode, error) {
	currToken, _ := token_set.Scanner.GetCurr()

	if token_set.ActParamList2Nil.Predict(currToken) {
		return nil, nil
	}
	if token_set.ActParamList2ActParamList.Predict(currToken) {
		res := []*tree_node.TreeNode{}
		if node, err := Exp(); err != nil {
			return nil, fmt.Errorf("ActParamList %v", err)
		} else {
			res = append(res, node)
		}
		if brothers, err := ActParamMore(); err != nil {
			return nil, fmt.Errorf("ActParamList %v", err)
		} else {
			res = append(res, brothers...)
		}
		return res, nil
	}

	return nil, fmt.Errorf("ActParamList match failed! %v", currToken)
}

func ActParamMore() ([]*tree_node.TreeNode, error) {
	currToken, _ := token_set.Scanner.GetCurr()

	if token_set.ActParamMore2Nil.Predict(currToken) {
		return nil, nil
	}
	if token_set.ActParamMore2ActParamList.Predict(currToken) {
		if _, err := Match(token_set.Comma); err != nil {
			return nil, fmt.Errorf("ActParamMore %v", err)
		}
		if params, err := ActParamList(); err != nil {
			return nil, fmt.Errorf("ActParamMore %v", err)
		} else {
			return params, nil
		}
	}

	return nil, fmt.Errorf("ActParamMore match failed! %v", currToken)
}
