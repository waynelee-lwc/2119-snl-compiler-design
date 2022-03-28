package statement

import (
	"fmt"
	"recursive_descent_parser/model/token_set"
	"recursive_descent_parser/model/tree_node"
)

func VarDec() (*tree_node.TreeNode, error) {
	currToken, _ := token_set.Scanner.GetCurr()

	if token_set.VarDec2Nil.Predict(currToken) {
		return nil, nil
	}
	if token_set.VarDec2VarDeclaration.Predict(currToken) {
		if node, err := VarDeclaration(); err != nil {
			return nil, fmt.Errorf("VarDec  %v", err)
		} else {
			return node, nil
		}
	}

	return nil, fmt.Errorf("VarDec match failed! %v", currToken)
}

func VarDeclaration() (*tree_node.TreeNode, error) {
	node := tree_node.NewTreeNode()
	node.NodeKind = tree_node.VarK

	if _, err := Match(token_set.Var); err != nil {
		return nil, fmt.Errorf("VarDeclaration  %v", err)
	}
	if children, err := VarDecList(); err != nil {
		return nil, fmt.Errorf("VarDeclaration parse fialed! %v", err)
	} else {
		node.Children = append(node.Children, children...)
	}

	return node, nil
}

func VarDecList() ([]*tree_node.TreeNode, error) {
	node := tree_node.NewTreeNode()
	node.NodeKind = tree_node.DecK
	res := []*tree_node.TreeNode{node}

	if err := TypeDef(node); err != nil {
		return nil, fmt.Errorf("VarDecList  %v", err)
	}
	if err := VarIdList(node); err != nil {
		return nil, fmt.Errorf("VarDecLIst  %v", err)
	}
	if _, err := Match(token_set.Semi); err != nil {
		return nil, fmt.Errorf("VarDecLIst  %v", err)
	}
	if brothers, err := VarDecMore(); err != nil {
		return nil, fmt.Errorf("VarDecLIst  %v", err)
	} else {
		res = append(res, brothers...)
	}

	return res, nil
}

func VarDecMore() ([]*tree_node.TreeNode, error) {
	currToken, _ := token_set.Scanner.GetCurr()

	if token_set.VarDecMore2Nil.Predict(currToken) {
		return nil, nil
	}
	if token_set.VarDecMore2VarDecList.Predict(currToken) {
		if brothers, err := VarDecList(); err != nil {
			return nil, fmt.Errorf("VarDecMore  %v", err)
		} else {
			return brothers, nil
		}
	}

	return nil, fmt.Errorf("VarDecMore match failed! %v", currToken)
}
