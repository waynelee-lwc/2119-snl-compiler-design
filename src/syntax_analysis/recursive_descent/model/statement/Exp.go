package statement

import (
	"fmt"
	"recursive_descent_parser/model/token_set"
	"recursive_descent_parser/model/tree_node"
)

func Exp() (*tree_node.TreeNode, error) {
	node := tree_node.NewTreeNode()
	node.NodeKind = tree_node.ExpK
	node.Attr.ExpAttr = &tree_node.ExpAttr{}

	if term, err := Term(); err != nil {
		return nil, fmt.Errorf("Exp %v", err)
	} else {
		node.Children = append(node.Children, term)
	}
	if otherTerm, err := OtherTerm(node); err != nil {
		return nil, fmt.Errorf("Exp %v", err)
	} else {
		if otherTerm != nil {
			// if node.Kind == tree_node.OpK && node.Attr.ExpAttr.Op == token_set.Minus.Name &&
			// 	otherTerm.Kind == tree_node.OpK && otherTerm.Attr.ExpAttr.Op == token_set.Minus.Name &&
			// 	!otherTerm.Attr.ExpAttr.Paren {
			// 	node.Children = append(node.Children, otherTerm.Children[0])
			// 	otherTerm.Children[0] = node
			// 	return otherTerm, nil
			// } else {
			node.Children = append(node.Children, otherTerm)
			return LeftRotate(node), nil
		} else {
			return node.Children[0], nil
		}
	}
}

func RelExp() (*tree_node.TreeNode, error) {
	node := tree_node.NewTreeNode()
	node.NodeKind = tree_node.ExpK
	node.Kind = tree_node.OpK
	node.Attr.ExpAttr = &tree_node.ExpAttr{}
	if exp, err := Exp(); err != nil {
		return nil, fmt.Errorf("RelExp %v", err)
	} else {
		node.Children = append(node.Children, exp)
	}
	if err := OtherRelE(node); err != nil {
		return nil, fmt.Errorf("RelExp %v", err)
	}

	return node, nil
}

func OtherRelE(node *tree_node.TreeNode) error {
	if err := CmpOp(node); err != nil {
		return fmt.Errorf("OtherRelE %v", err)
	}
	if exp, err := Exp(); err != nil {
		return fmt.Errorf("OtherRelE %v", err)
	} else {
		node.Children = append(node.Children, exp)
	}
	return nil
}

func Term() (*tree_node.TreeNode, error) {
	node := tree_node.NewTreeNode()
	node.NodeKind = tree_node.ExpK
	node.Attr.ExpAttr = &tree_node.ExpAttr{}
	if factor, err := Factor(); err != nil {
		return nil, fmt.Errorf("Term %v", err)
	} else {
		node.Children = append(node.Children, factor)
	}
	if otherFactor, err := OtherFactor(node); err != nil {
		return nil, fmt.Errorf("Term %v", err)
	} else {
		if otherFactor == nil {
			return node.Children[0], nil
		} else {
			node.Children = append(node.Children, otherFactor)
			return LeftRotate(node), nil
		}
	}
}

func Factor() (*tree_node.TreeNode, error) {
	currToken, _ := token_set.Scanner.GetCurr()

	if token_set.Factor2Exp.Predict(currToken) {
		var node *tree_node.TreeNode = nil
		if _, err := Match(token_set.LParen); err != nil {
			return nil, fmt.Errorf("Factor %v", err)
		}
		if exp, err := Exp(); err != nil {
			return nil, fmt.Errorf("Factor %v", err)
		} else {
			node = exp
		}
		if _, err := Match(token_set.RParen); err != nil {
			return nil, fmt.Errorf("Factor %v", err)
		}
		node.Attr.ExpAttr.Paren = true //括号包裹表达式
		return node, nil
	}
	if token_set.Factor2IntC.Predict(currToken) {
		node := tree_node.NewTreeNode()
		node.NodeKind = tree_node.ExpK
		node.Kind = tree_node.ConstK
		node.Attr.ExpAttr = &tree_node.ExpAttr{}
		if intc, err := Match(token_set.Number); err != nil {
			return nil, fmt.Errorf("Factor %v", err)
		} else {
			node.Attr.ExpAttr.Val = intc.Name
			return node, nil
		}
	}
	if token_set.Factor2Variable.Predict(currToken) {
		if variable, err := Variable(); err != nil {
			return nil, fmt.Errorf("Factor %v", err)
		} else {
			return variable, nil
		}
	}
	if token_set.Factor2CharC.Predict(currToken) {
		//赋值可以是单个字符
		node := tree_node.NewTreeNode()
		node.NodeKind = tree_node.ExpK
		node.Kind = tree_node.ConstK
		node.Attr.ExpAttr = &tree_node.ExpAttr{}
		if charc, err := Match(token_set.Charc); err != nil {
			return nil, fmt.Errorf("Factor %v", err)
		} else {
			node.Attr.ExpAttr.Val = "'" + charc.Name + "'"
			return node, nil
		}
	}

	return nil, fmt.Errorf("Factor match failed! %v", currToken)
}

func OtherFactor(node *tree_node.TreeNode) (*tree_node.TreeNode, error) {
	currToken, _ := token_set.Scanner.GetCurr()

	if token_set.OtherFactor2Nil.Predict(currToken) {
		return nil, nil
	}
	if token_set.OtherFactor2MultOp.Predict(currToken) {
		if err := MultOp(node); err != nil {
			return nil, fmt.Errorf("OtherFactor %v", err)
		}
		if term, err := Term(); err != nil {
			return nil, fmt.Errorf("OtherFactor %v", err)
		} else {
			return term, nil
		}
	}

	return nil, fmt.Errorf("OtherFac match failed! %v", currToken)
}

func OtherTerm(node *tree_node.TreeNode) (*tree_node.TreeNode, error) {
	currToken, _ := token_set.Scanner.GetCurr()

	if token_set.OtherTerm2Nil.Predict(currToken) {
		return nil, nil
	}
	if token_set.OtherTerm2AddOp.Predict(currToken) {
		if err := AddOp(node); err != nil {
			return nil, fmt.Errorf("OtherTerm %v", err)
		}
		if exp, err := Exp(); err != nil {
			return nil, fmt.Errorf("OtherTerm %v", err)
		} else {
			return exp, nil
		}
	}

	return nil, fmt.Errorf("OtherTerm match failed! %v", currToken)
}

func Variable() (*tree_node.TreeNode, error) {
	node := tree_node.NewTreeNode()
	node.NodeKind = tree_node.ExpK
	node.Kind = tree_node.IdK
	node.Attr.ExpAttr = &tree_node.ExpAttr{}
	if id, err := Match(token_set.ID); err != nil {
		return nil, fmt.Errorf("Variable %v", err)
	} else {
		node.Name = append(node.Name, id.Name)
	}
	if err := VariMore(node); err != nil {
		return nil, fmt.Errorf("Variable %v", err)
	}

	return node, nil
}

func VariMore(node *tree_node.TreeNode) error {
	currToken, _ := token_set.Scanner.GetCurr()

	if token_set.VariMore2Nil.Predict(currToken) {
		node.Attr.ExpAttr.VarKind = tree_node.IdV
		return nil
	}
	if token_set.VariMore2Exp.Predict(currToken) {
		node.Attr.ExpAttr.VarKind = tree_node.ArrayMembV
		if _, err := Match(token_set.LMidParen); err != nil {
			return fmt.Errorf("VariMore %v", err)
		}
		if exp, err := Exp(); err != nil {
			return fmt.Errorf("VariMore %v", err)
		} else {
			node.Children = append(node.Children, exp)
		}
		if _, err := Match(token_set.RMidParen); err != nil {
			return fmt.Errorf("VariMore %v", err)
		}
		return nil
	}
	if token_set.VariMore2FieldVar.Predict(currToken) {
		node.Attr.ExpAttr.VarKind = tree_node.FieldMembV
		if _, err := Match(token_set.Dot); err != nil {
			return fmt.Errorf("VariMore %v", err)
		}
		if fieldVar, err := FieldVar(); err != nil {
			return fmt.Errorf("VariMore %v", err)
		} else {
			node.Children = append(node.Children, fieldVar)
		}
		return nil
	}

	return fmt.Errorf("VariMore match failed! %v", currToken)
}

func FieldVar() (*tree_node.TreeNode, error) {
	node := tree_node.NewTreeNode()
	node.NodeKind = tree_node.ExpK
	node.Kind = tree_node.IdK
	node.Attr.ExpAttr = &tree_node.ExpAttr{}

	if id, err := Match(token_set.ID); err != nil {
		return nil, fmt.Errorf("FieldVar %v", err)
	} else {
		node.Name = append(node.Name, id.Name)
	}
	if err := FieldVarMore(node); err != nil {
		return nil, fmt.Errorf("FieldVar %v", err)
	}

	return node, nil
}

func FieldVarMore(node *tree_node.TreeNode) error {
	currToken, _ := token_set.Scanner.GetCurr()
	node.Attr.ExpAttr = &tree_node.ExpAttr{}

	if token_set.FieldVarMore2Nil.Predict(currToken) {
		node.Attr.ExpAttr.VarKind = tree_node.IdV
		return nil
	}
	if token_set.FieldVarMore2Exp.Predict(currToken) {
		node.Attr.ExpAttr.VarKind = tree_node.ArrayMembV
		if _, err := Match(token_set.LMidParen); err != nil {
			return fmt.Errorf("FieldVarMore %v", err)
		}
		if exp, err := Exp(); err != nil {
			return fmt.Errorf("FieldVarMore %v", err)
		} else {
			node.Children = append(node.Children, exp)
		}
		if _, err := Match(token_set.RMidParen); err != nil {
			return fmt.Errorf("FieldVarMore %v", err)
		}
		return nil
	}

	return fmt.Errorf("FieldVarMore match failed! %v", currToken)
}

func CmpOp(node *tree_node.TreeNode) error {
	currToken, _ := token_set.Scanner.GetCurr()
	node.Kind = tree_node.OpK
	node.Attr.ExpAttr = &tree_node.ExpAttr{}

	if token_set.CmpOp2EQ.Predict(currToken) {
		if op, err := Match(token_set.Equal); err != nil {
			return fmt.Errorf("CmpOp %v", err)
		} else {
			node.Attr.ExpAttr.Op = op.Name
			return nil
		}
	}
	if token_set.CmpOp2LT.Predict(currToken) {
		if op, err := Match(token_set.LT); err != nil {
			return fmt.Errorf("CmpOp %v", err)
		} else {
			node.Attr.ExpAttr.Op = op.Name
			return nil
		}
	}

	return fmt.Errorf("CmpOp match failed! %v", currToken)
}

func AddOp(node *tree_node.TreeNode) error {
	currToken, _ := token_set.Scanner.GetCurr()
	node.Kind = tree_node.OpK
	node.Attr.ExpAttr = &tree_node.ExpAttr{}

	if token_set.AddOp2Plus.Predict(currToken) {
		if op, err := Match(token_set.Plus); err != nil {
			return fmt.Errorf("CmpOp %v", err)
		} else {
			node.Attr.ExpAttr.Op = op.Name
			return nil
		}
	}
	if token_set.AddOp2Minus.Predict(currToken) {
		if op, err := Match(token_set.Minus); err != nil {
			return fmt.Errorf("CmpOp %v", err)
		} else {
			node.Attr.ExpAttr.Op = op.Name
			return nil
		}
	}

	return fmt.Errorf("CmpOp match failed! %v", currToken)
}

func MultOp(node *tree_node.TreeNode) error {
	currToken, _ := token_set.Scanner.GetCurr()
	node.Kind = tree_node.OpK
	node.Attr.ExpAttr = &tree_node.ExpAttr{}

	if token_set.MultOp2Times.Predict(currToken) {
		if op, err := Match(token_set.Times); err != nil {
			return fmt.Errorf("CmpOp %v", err)
		} else {
			node.Attr.ExpAttr.Op = op.Name
			return nil
		}
	}
	if token_set.MultOp2Over.Predict(currToken) {
		if op, err := Match(token_set.Over); err != nil {
			return fmt.Errorf("CmpOp %v", err)
		} else {
			node.Attr.ExpAttr.Op = op.Name
			return nil
		}
	}

	return fmt.Errorf("CmpOp match failed! %v", currToken)
}

func LeftRotate(node *tree_node.TreeNode) *tree_node.TreeNode {

	rson := node.Children[1]
	if NeedLeftRotate(node, rson) {

		rlson := rson.Children[0]
		node.Children[1] = rlson
		rson.Children[0] = LeftRotate(node)
		return rson
	} else {
		return node
	}
}

func NeedLeftRotate(node *tree_node.TreeNode, rson *tree_node.TreeNode) bool {

	if node.NodeKind != tree_node.ExpK || rson.NodeKind != tree_node.ExpK {
		return false
	}

	if node.Kind != tree_node.OpK || rson.Kind != tree_node.OpK {
		return false
	}

	if (node.Attr.ExpAttr.Op == "+" || node.Attr.ExpAttr.Op == "-") &&
		(rson.Attr.ExpAttr.Op == "+" || rson.Attr.ExpAttr.Op == "-") &&
		!rson.Attr.ExpAttr.Paren {
		return true
	}

	if (node.Attr.ExpAttr.Op == "*" || node.Attr.ExpAttr.Op == "/") &&
		(rson.Attr.ExpAttr.Op == "*" || rson.Attr.ExpAttr.Op == "/") &&
		!rson.Attr.ExpAttr.Paren {
		return true
	}
	return false
}
