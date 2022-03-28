package statement

import (
	"fmt"
	"recursive_descent_parser/model/token_set"
	"recursive_descent_parser/model/tree_node"
)

func StmList() ([]*tree_node.TreeNode, error) {
	res := []*tree_node.TreeNode{}

	if node, err := Stm(); err != nil {
		return nil, fmt.Errorf("StmList %v", err)
	} else {
		res = append(res, node)
	}
	if brothers, err := StmMore(); err != nil {
		return nil, fmt.Errorf("StmList %v", err)
	} else {
		res = append(res, brothers...)
	}

	return res, nil
}

func StmMore() ([]*tree_node.TreeNode, error) {
	currToken, _ := token_set.Scanner.GetCurr()

	if token_set.StmMore2Nil.Predict(currToken) {
		return nil, nil
	}
	if token_set.StmMore2StmList.Predict(currToken) {
		if _, err := Match(token_set.Semi); err != nil {
			return nil, fmt.Errorf("StmMore %v", err)
		}
		if brothers, err := StmList(); err != nil {
			return nil, fmt.Errorf("StmMore %v", err)
		} else {
			return brothers, nil
		}
	}

	return nil, fmt.Errorf("StmMore match failed! %v", currToken)
}

func Stm() (*tree_node.TreeNode, error) {
	currToken, _ := token_set.Scanner.GetCurr()

	if token_set.Stm2ConditionalStm.Predict(currToken) {
		if node, err := ConditionalStm(); err != nil {
			return nil, fmt.Errorf("Stm %v", err)
		} else {
			return node, nil
		}
	}
	if token_set.Stm2LoopStm.Predict(currToken) {
		if node, err := LoopStm(); err != nil {
			return nil, fmt.Errorf("Stm %v", err)
		} else {
			return node, nil
		}
	}
	if token_set.Stm2InputStm.Predict(currToken) {
		if node, err := InputStm(); err != nil {
			return nil, fmt.Errorf("Stm %v", err)
		} else {
			return node, nil
		}
	}
	if token_set.Stm2OutputStm.Predict(currToken) {
		if node, err := OutputStm(); err != nil {
			return nil, fmt.Errorf("Stm %v", err)
		} else {
			return node, nil
		}
	}
	if token_set.Stm2ReturnStm.Predict(currToken) {
		if node, err := ReturnStm(); err != nil {
			return nil, fmt.Errorf("Stm %v", err)
		} else {
			return node, nil
		}
	}
	//这里用match Id的话无法给结构赋值
	if token_set.Stm2AssCal.Predict(currToken) {
		idNode := tree_node.NewTreeNode()
		idNode.NodeKind = tree_node.ExpK
		idNode.Kind = tree_node.IdK
		idNode.Attr.ExpAttr = &tree_node.ExpAttr{}
		if id, err := Match(token_set.ID); err != nil {
			return nil, fmt.Errorf("Stm %v", err)
		} else {
			idNode.Name = append(idNode.Name, id.Name)
			idNode.IdNum++
		}
		if node, err := AssCall(idNode); err != nil {
			return nil, fmt.Errorf("Stm %v", err)
		} else {
			return node, nil
		}
	}

	return nil, fmt.Errorf("Stm match failed! %v", currToken)
}

func AssCall(idNode *tree_node.TreeNode) (*tree_node.TreeNode, error) {
	currToken, _ := token_set.Scanner.GetCurr()

	if token_set.AssCall2AssignmentRest.Predict(currToken) {
		if node, err := AssignmentRest(idNode); err != nil {
			return nil, fmt.Errorf("AssCall %v", err)
		} else {
			return node, nil
		}
	}
	if token_set.AssCall2CallStmRest.Predict(currToken) {
		if node, err := CallStmRest(idNode); err != nil {
			return nil, fmt.Errorf("AssCall %v", err)
		} else {
			return node, nil
		}
	}

	return nil, fmt.Errorf("AssCall match failed! %v", currToken)
}

func AssignmentRest(idNode *tree_node.TreeNode) (*tree_node.TreeNode, error) {
	node := tree_node.NewTreeNode()
	node.NodeKind = tree_node.StmtK
	node.Kind = tree_node.AssignK
	node.Children = append(node.Children, idNode)

	//这里应该加上VariMore
	if err := VariMore(idNode); err != nil {
		return nil, fmt.Errorf("AssignmentRest %v", err)
	}

	if _, err := Match(token_set.Assign); err != nil {
		return nil, fmt.Errorf("AssignmentRest %v", err)
	}
	if exp, err := Exp(); err != nil {
		return nil, fmt.Errorf("AssignmentRest %v", err)
	} else {
		node.Children = append(node.Children, exp)
	}

	return node, nil
}

func ConditionalStm() (*tree_node.TreeNode, error) {
	node := tree_node.NewTreeNode()
	node.NodeKind = tree_node.StmtK
	node.Kind = tree_node.IfK

	if _, err := Match(token_set.If); err != nil { //IF
		return nil, fmt.Errorf("ConditionalStm %v", err)
	}
	if exp, err := RelExp(); err != nil { //RelE
		return nil, fmt.Errorf("ConditionalStm %v", err)
	} else {
		node.Children = append(node.Children, exp)
	}
	if _, err := Match(token_set.Then); err != nil { //THEN
		return nil, fmt.Errorf("ConditionalStm %v", err)
	}
	if stmL, err := StmList(); err != nil { //StmList
		return nil, fmt.Errorf("ConditionalStm %v", err)
	} else {
		node.Children = append(node.Children, stmL...)
	}
	if _, err := Match(token_set.Else); err != nil { //ELSE
		return nil, fmt.Errorf("ConditionalStm %v", err)
	}
	if stmL, err := StmList(); err != nil { //StmList
		return nil, fmt.Errorf("ConditionalStm %v", err)
	} else {
		node.Children = append(node.Children, stmL...)
	}
	if _, err := Match(token_set.Fi); err != nil { //FI
		return nil, fmt.Errorf("ConditionalStm %v", err)
	}

	return node, nil
}

func LoopStm() (*tree_node.TreeNode, error) {
	node := tree_node.NewTreeNode()
	node.NodeKind = tree_node.StmtK
	node.Kind = tree_node.WhileK

	if _, err := Match(token_set.While); err != nil { //WHILE
		return nil, fmt.Errorf("LoopStm %v", err)
	}
	if exp, err := RelExp(); err != nil { //RelExp
		return nil, fmt.Errorf("LoopStm %v", err)
	} else {
		node.Children = append(node.Children, exp)
	}
	if _, err := Match(token_set.Do); err != nil { //DO
		return nil, fmt.Errorf("LoopStm %v", err)
	}
	if stmL, err := StmList(); err != nil { //StmList
		return nil, fmt.Errorf("LoopStm %v", err)
	} else {
		node.Children = append(node.Children, stmL...)
	}
	if _, err := Match(token_set.EndWhile); err != nil { //ENDWH
		return nil, fmt.Errorf("LoopStm %v", err)
	}

	return node, nil
}

func InputStm() (*tree_node.TreeNode, error) {
	node := tree_node.NewTreeNode()
	node.NodeKind = tree_node.StmtK
	node.Kind = tree_node.ReadK

	if _, err := Match(token_set.Read); err != nil {
		return nil, fmt.Errorf("InputStm %v", err)
	}
	if _, err := Match(token_set.LParen); err != nil {
		return nil, fmt.Errorf("InputStm %v", err)
	}
	if id, err := Match(token_set.ID); err != nil {
		return nil, fmt.Errorf("InputStm %v", err)
	} else {
		node.Name = append(node.Name, id.Name)
	}
	if _, err := Match(token_set.RParen); err != nil {
		return nil, fmt.Errorf("InputStm %v", err)
	}

	return node, nil
}

func OutputStm() (*tree_node.TreeNode, error) {
	node := tree_node.NewTreeNode()
	node.NodeKind = tree_node.StmtK
	node.Kind = tree_node.WriteK

	if _, err := Match(token_set.Write); err != nil {
		return nil, fmt.Errorf("OutputStm %v", err)
	}
	if _, err := Match(token_set.LParen); err != nil {
		return nil, fmt.Errorf("OutputStm %v", err)
	}
	if exp, err := Exp(); err != nil {
		return nil, fmt.Errorf("OutputStm %v", err)
	} else {
		node.Children = append(node.Children, exp)
	}
	if _, err := Match(token_set.RParen); err != nil {
		return nil, fmt.Errorf("OutputStm %v", err)
	}

	return node, nil
}

func ReturnStm() (*tree_node.TreeNode, error) {
	node := tree_node.NewTreeNode()
	node.NodeKind = tree_node.StmtK
	node.Kind = tree_node.ReturnK

	if _, err := Match(token_set.Return); err != nil {
		return nil, fmt.Errorf("ReturnStm %v", err)
	}

	return node, nil
}
func CallStmRest(idNode *tree_node.TreeNode) (*tree_node.TreeNode, error) {
	node := tree_node.NewTreeNode()
	node.NodeKind = tree_node.StmtK
	node.Kind = tree_node.CallK
	node.Children = append(node.Children, idNode)

	if _, err := Match(token_set.LParen); err != nil {
		return nil, fmt.Errorf("CallStmRest %v", err)
	}
	if params, err := ActParamList(); err != nil {
		return nil, fmt.Errorf("CallStmRest %v", err)
	} else {
		node.Children = append(node.Children, params...)
	}
	if _, err := Match(token_set.RParen); err != nil {
		return nil, fmt.Errorf("CallStmRest %v", err)
	}

	return node, nil
}
