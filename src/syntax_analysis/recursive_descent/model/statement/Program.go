package statement

import (
	"fmt"
	"recursive_descent_parser/model/token_set"
	"recursive_descent_parser/model/tree_node"
)

func Program() (*tree_node.TreeNode, error) {
	node := tree_node.NewTreeNode()
	node.NodeKind = tree_node.ProK
	if programHead, err := ProgramHead(); err != nil {
		return nil, fmt.Errorf("Program parse failed! %v", err)
	} else {
		node.Children = append(node.Children, programHead)
	}

	if declarations, err := DeclarePart(); err != nil {
		return nil, fmt.Errorf("Program parse failed! %v", err)
	} else {
		node.Children = append(node.Children, declarations...)
	}

	if programBody, err := ProgramBody(); err != nil {
		return nil, fmt.Errorf("Program parse failed! %v", err)
	} else {
		node.Children = append(node.Children, programBody)
	}

	return node, nil
}

func ProgramHead() (*tree_node.TreeNode, error) {
	node := tree_node.NewTreeNode()
	node.NodeKind = tree_node.PheadK
	if _, err := Match(token_set.Program); err != nil {
		return nil, fmt.Errorf("ProgramHead parse failed! %v", err)
	}

	if err := ProgramName(node); err != nil {
		return nil, fmt.Errorf("ProgramHead parse failed! %v", err)
	}

	return node, nil
}

func ProgramName(node *tree_node.TreeNode) error {
	if name, err := Match(token_set.ID); err != nil {
		return fmt.Errorf("ProgramName parse failed! %v", err)
	} else {
		node.Name = append(node.Name, name.Name)
	}

	return nil
}

func DeclarePart() ([]*tree_node.TreeNode, error) {
	res := []*tree_node.TreeNode{}

	if typeDec, err := TypeDec(); err != nil {
		return nil, fmt.Errorf("DeclarePart parse failed! %v", err)
	} else {
		res = append(res, typeDec)
	}

	if varDec, err := VarDec(); err != nil {
		return nil, fmt.Errorf("DeclarePart parse failed! %v", err)
	} else {
		res = append(res, varDec)
	}

	if procDecs, err := ProcDec(); err != nil {
		return nil, fmt.Errorf("DeclarePart parse failed! %v", err)
	} else {
		res = append(res, procDecs...)
	}

	return res, nil
}

func ProgramBody() (*tree_node.TreeNode, error) {

	return nil, nil
}
