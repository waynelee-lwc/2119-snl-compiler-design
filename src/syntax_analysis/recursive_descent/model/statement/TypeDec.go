package statement

import (
	"fmt"
	"recursive_descent_parser/model/token_set"
	"recursive_descent_parser/model/tree_node"
	"strconv"
)

func TypeDec() (*tree_node.TreeNode, error) {
	currToken, err := token_set.Scanner.GetCurr()

	if token_set.TypeDec2Nil.Predict(currToken) {
		return nil, nil
	}

	if token_set.TypeDec2TypeDeclaration.Predict(currToken) {
		node, err := TypeDeclaration()
		if err != nil {
			return nil, fmt.Errorf("TypeDec  %v", err)
		}
		return node, nil

	}

	return nil, fmt.Errorf("TypeDec match failed! %v,%v", currToken, err)
}

func TypeDeclaration() (*tree_node.TreeNode, error) {
	node := tree_node.NewTreeNode()
	node.NodeKind = tree_node.TypeK

	_, err := Match(token_set.Type)
	if err != nil {
		return nil, fmt.Errorf("TypeDeclaration  %v", err)
	}

	chilren, err := TypeDecList()
	node.Children = append(node.Children, chilren...)

	return node, err
}

func TypeDecList() ([]*tree_node.TreeNode, error) {
	node := tree_node.NewTreeNode()
	node.NodeKind = tree_node.DecK

	if err := TypeId(node); err != nil {
		return nil, fmt.Errorf("TypeDecList  %v", err)
	}
	if _, err := Match(token_set.Equal); err != nil {
		return nil, fmt.Errorf("TypeDecList  %v", err)
	}
	if err := TypeDef(node); err != nil {
		return nil, fmt.Errorf("TypeDecList  %v", err)
	}
	if _, err := Match(token_set.Semi); err != nil {
		return nil, fmt.Errorf("TypeDecList  %v", err)
	}

	brothers, err := TypeDecMore()
	if err != nil {
		return nil, fmt.Errorf("TypeDecList  %v", err)
	}
	res := []*tree_node.TreeNode{node}
	return append(res, brothers...), nil
}

func TypeDecMore() ([]*tree_node.TreeNode, error) {
	currToken, _ := token_set.Scanner.GetCurr()

	if token_set.TypeDecMore2Nil.Predict(currToken) {
		return nil, nil
	}
	if token_set.TypeDecMore2TypeDecList.Predict(currToken) {
		brothers, err := TypeDecList()
		if err != nil {
			return nil, fmt.Errorf("TypeDecMore  %v", err)
		}
		return brothers, nil
	}
	return nil, fmt.Errorf("TypeDecMore match failed! %v", currToken)
}

func TypeId(node *tree_node.TreeNode) error {
	match, err := Match(token_set.ID)
	if err != nil {
		return fmt.Errorf("TypeId match failed! %v", err)
	}
	node.Name = append(node.Name, match.Name)
	node.IdNum++
	return nil
}

func TypeDef(node *tree_node.TreeNode) error {
	currToken, _ := token_set.Scanner.GetCurr()

	if token_set.TypeDef2BaseType.Predict(currToken) {
		if baseType, err := BaseType(); err != nil {
			return fmt.Errorf("TypeDef  %v", err)
		} else {
			node.Kind = baseType
			return nil
		}
	}
	if token_set.TypeDef2StructureType.Predict(currToken) {
		if err := StructureType(node); err != nil {
			return fmt.Errorf("TypeDef  %v", err)
		}
		return nil
	}
	if token_set.TypeDef2Id.Predict(currToken) {
		if match, err := Match(token_set.ID); err != nil {
			return fmt.Errorf("TypeDef  %v", err)
		} else {
			node.TypeName = match.Name
			node.Kind = tree_node.IdK
			return nil
		}
	}

	return fmt.Errorf("TypeDef  %v", currToken)
}

func StructureType(node *tree_node.TreeNode) error {
	currToken, _ := token_set.Scanner.GetCurr()

	if token_set.StructureType2ArrayType.Predict(currToken) {
		if err := ArrayType(node); err != nil {
			return fmt.Errorf("StructureType %v", err)
		}
		return nil
	}
	if token_set.StructureTYpe2RecType.Predict(currToken) {
		if err := RecType(node); err != nil {
			return fmt.Errorf("StructureType %v", err)
		}
		return nil
	}

	return fmt.Errorf("StructureType match failed! %v", currToken)
}

func ArrayType(node *tree_node.TreeNode) error {
	node.Kind = tree_node.ArrayK
	node.Attr.ArrayAttr = &tree_node.ArrayAttr{}

	if _, err := Match(token_set.Array); err != nil {
		//ARRAY
		return fmt.Errorf("ArrayType  %v", err)
	}
	if _, err := Match(token_set.LMidParen); err != nil {
		//[
		return fmt.Errorf("ArrayType  %v", err)
	}
	if low, err := Match(token_set.Number); err != nil {
		//low
		return fmt.Errorf("ArrayType  %v", err)
	} else {
		node.Attr.ArrayAttr.Low, _ = strconv.Atoi(low.Name)
	}
	if _, err := Match(token_set.Range); err != nil {
		//..
		return fmt.Errorf("ArrayType  %v", err)
	}
	if top, err := Match(token_set.Number); err != nil {
		//top
		return fmt.Errorf("ArrayType  %v", err)
	} else {
		node.Attr.ArrayAttr.Top, _ = strconv.Atoi(top.Name)
	}
	if _, err := Match(token_set.RMidParen); err != nil {
		//]
		return fmt.Errorf("ArrayType  %v", err)
	}
	if _, err := Match(token_set.Of); err != nil {
		//of
		return fmt.Errorf("ArrayType  %v", err)
	}
	if baseType, err := BaseType(); err != nil {
		//BaseType
		return fmt.Errorf("ArrayType  %v", err)
	} else {
		node.Attr.ArrayAttr.ChildType = tree_node.BaseType2ChildType[baseType]
	}

	return nil
}

func RecType(node *tree_node.TreeNode) error {
	node.Kind = tree_node.RecordK
	if _, err := Match(token_set.Record); err != nil {
		return fmt.Errorf("RecType  %v", err)
	}
	if children, err := FieldDecList(); err != nil {
		return fmt.Errorf("RecType  %v", err)
	} else {
		node.Children = children
	}
	if _, err := Match(token_set.End); err != nil {
		return fmt.Errorf("RecType  %v", err)
	}
	return nil
}

func FieldDecList() ([]*tree_node.TreeNode, error) {
	currToken, _ := token_set.Scanner.GetCurr()
	node := tree_node.NewTreeNode()
	node.NodeKind = tree_node.DecK
	node.Attr.ProcAttr = &tree_node.ProcAttr{}
	res := []*tree_node.TreeNode{node}

	if token_set.FieldDecList2BaseType.Predict(currToken) {
		if baseType, err := BaseType(); err != nil {
			return nil, fmt.Errorf("FieldDecList  %v", err)
		} else {
			node.Kind = baseType
		}
		if err := IdList(node); err != nil {
			return nil, fmt.Errorf("FieldDecList  %v", err)
		}
		if _, err := Match(token_set.Semi); err != nil {
			return nil, fmt.Errorf("FieldDecList  %v", err)
		}
		if brothers, err := FieldDecMore(); err != nil {
			return nil, fmt.Errorf("FieldDecList  %v", err)
		} else {
			res = append(res, brothers...)
			return res, nil
		}
	}
	if token_set.FieldDecList2ArrayType.Predict(currToken) {
		if err := ArrayType(node); err != nil {
			return nil, fmt.Errorf("FieldDecList  %v", err)
		}
		if err := IdList(node); err != nil {
			return nil, fmt.Errorf("FieldDecList  %v", err)
		}
		if _, err := Match(token_set.Semi); err != nil {
			return nil, fmt.Errorf("FieldDecList  %v", err)
		}
		if brothers, err := FieldDecMore(); err != nil {
			return nil, fmt.Errorf("FieldDecList  %v", err)
		} else {
			res = append(res, brothers...)
			return res, nil
		}
	}

	return nil, fmt.Errorf("FieldDecList match failed! %v", currToken)
}

func FieldDecMore() ([]*tree_node.TreeNode, error) {
	currToken, _ := token_set.Scanner.GetCurr()

	if token_set.FieldDecMore2Nil.Predict(currToken) {
		return nil, nil
	}
	if token_set.FieldDecMore2FieldDecList.Predict(currToken) {
		if brothers, err := FieldDecList(); err != nil {
			return nil, fmt.Errorf("FieldDecMore  %v", err)
		} else {
			return brothers, nil
		}
	}

	return nil, fmt.Errorf("FieldDecMore match failed! %v", currToken)
}
