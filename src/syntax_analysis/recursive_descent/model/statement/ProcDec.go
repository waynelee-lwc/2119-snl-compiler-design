package statement

import (
	"fmt"
	"recursive_descent_parser/model/token_set"
	"recursive_descent_parser/model/tree_node"
)

func ProcDec() ([]*tree_node.TreeNode, error) {
	currToken, _ := token_set.Scanner.GetCurr()

	if token_set.ProcDec2Nil.Predict(currToken) {
		return nil, nil
	}
	if token_set.ProcDec2ProcDeclaration.Predict(currToken) {
		if nodes, err := ProcDeclaration(); err != nil {
			return nil, fmt.Errorf("ProDec  %v", err)
		} else {
			return nodes, nil
		}
	}

	return nil, fmt.Errorf("ProcDec match failed! %v", currToken)
}

func ProcDeclaration() ([]*tree_node.TreeNode, error) {
	node := tree_node.NewTreeNode()
	node.NodeKind = tree_node.ProcDecK
	res := []*tree_node.TreeNode{node}
	if _, err := Match(token_set.Procedure); err != nil {
		return nil, fmt.Errorf("ProDeclaration  %v", err)
	}
	if err := ProcName(node); err != nil {
		return nil, fmt.Errorf("ProDeclaration  %v", err)
	}
	if _, err := Match(token_set.LParen); err != nil {
		return nil, fmt.Errorf("ProDeclaration  %v", err)
	}
	// if childern, err := ParamDecList(); err != nil {
	// 	return nil, fmt.Errorf("ProDeclaration  %v", err)
	// } else {
	// 	node.Children = append(node.Children, childern...)
	// }
	if err := ParamList(node); err != nil {
		return nil, fmt.Errorf("ProDeclaration  %v", err)
	}
	if _, err := Match(token_set.RParen); err != nil {
		return nil, fmt.Errorf("ProDeclaration  %v", err)
	}
	if _, err := Match(token_set.Semi); err != nil {
		return nil, fmt.Errorf("ProDeclaration %v", err)
	}

	if procDecPart, err := ProcDecPart(); err != nil {
		return nil, fmt.Errorf("ProcDeclaration %v", err)
	} else {
		node.Children = append(node.Children, procDecPart...)
	}

	if procBody, err := ProcBody(); err != nil {
		return nil, fmt.Errorf("ProcDeclaration %v", err)
	} else {
		node.Children = append(node.Children, procBody)
	}

	if brothers, err := ProcDecMore(); err != nil {
		return nil, fmt.Errorf("ProDeclaration  %v", err)
	} else {
		res = append(res, brothers...)
	}

	return res, nil
}

func ProcDecPart() ([]*tree_node.TreeNode, error) {
	if node, err := DeclarePart(); err != nil {
		return nil, fmt.Errorf("ProcDecPart %v", err)
	} else {
		return node, err
	}
}

func ProcBody() (*tree_node.TreeNode, error) {
	if node, err := ProgramBody(); err != nil {
		return nil, fmt.Errorf("ProcBody, %v", err)
	} else {
		return node, nil
	}
}

func ProcName(node *tree_node.TreeNode) error {
	if id, err := Match(token_set.ID); err != nil {
		return fmt.Errorf("ProcName  %v", err)
	} else {
		node.Name = append(node.Name, id.Name)
	}

	return nil
}

func ProcDecMore() ([]*tree_node.TreeNode, error) {
	currToken, _ := token_set.Scanner.GetCurr()

	if token_set.ProcDecMore2Nil.Predict(currToken) {
		return nil, nil
	}
	if token_set.ProcDecMore2ProcDec.Predict(currToken) {
		if brothers, err := ProcDeclaration(); err != nil {
			return nil, fmt.Errorf("ProcDecMore  %v", err)
		} else {
			return brothers, nil
		}
	}

	return nil, fmt.Errorf("ProcDecMore match failed! %v", currToken)
}

func ParamList(node *tree_node.TreeNode) error {
	currToken, _ := token_set.Scanner.GetCurr()

	if token_set.ParamList2Nil.Predict(currToken) {
		return nil
	}
	if token_set.ParamList2ParamDecList.Predict(currToken) {
		if children, err := ParamDecList(); err != nil {
			return fmt.Errorf("ParamList failed failed! %v", err)
		} else {
			node.Children = append(node.Children, children...)
			return nil
		}
	}

	return fmt.Errorf("ParamList match failed! %v", currToken)
}

func ParamDecList() ([]*tree_node.TreeNode, error) {
	res := []*tree_node.TreeNode{}
	if node, err := Param(); err != nil {
		return nil, fmt.Errorf("ParamDecList  %v", err)
	} else {
		res = append(res, node)
	}
	if brothers, err := ParamMore(); err != nil {
		return nil, fmt.Errorf("ParamDecList  %v", err)
	} else {
		res = append(res, brothers...)
	}

	return res, nil
}

func ParamMore() ([]*tree_node.TreeNode, error) {
	currToken, _ := token_set.Scanner.GetCurr()

	if token_set.ParamMore2Nil.Predict(currToken) {
		return nil, nil
	}
	if token_set.ParamMore2ParamDecList.Predict(currToken) {
		if _, err := Match(token_set.Semi); err != nil {
			return nil, fmt.Errorf("ParamMore  %v", err)
		}
		if nodes, err := ParamDecList(); err != nil {
			return nil, fmt.Errorf("ParamMore  %v", err)
		} else {
			return nodes, nil
		}
	}

	return nil, fmt.Errorf("ParamMore match failed! %v", currToken)
}

func Param() (*tree_node.TreeNode, error) {
	currToken, _ := token_set.Scanner.GetCurr()
	node := tree_node.NewTreeNode()
	node.NodeKind = tree_node.DecK
	node.Attr.ProcAttr = &tree_node.ProcAttr{}

	if token_set.ParamVal.Predict(currToken) {
		node.Attr.ProcAttr.ParamType = tree_node.ValParamType
		if err := TypeDef(node); err != nil {
			return nil, fmt.Errorf("Param  %v", err)
		}
		if err := FormList(node); err != nil {
			return nil, fmt.Errorf("Param  %v", err)
		}
		return node, nil
	}
	if token_set.ParamVar.Predict(currToken) {
		node.Attr.ProcAttr.ParamType = tree_node.VarParamType
		if _, err := Match(token_set.Var); err != nil {
			return nil, fmt.Errorf("Param  %v", err)
		}
		if err := TypeDef(node); err != nil {
			return nil, fmt.Errorf("Param  %v", err)
		}
		if err := FormList(node); err != nil {
			return nil, fmt.Errorf("Param  %v", err)
		}
		return node, nil
	}
	return nil, fmt.Errorf("Param match failed! %v", currToken)
}
