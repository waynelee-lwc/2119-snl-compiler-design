package tree_node

import (
	"strconv"
)

type NodeKind string      //语法树节点类型
type Kind string          //语法树节点具体类型
type ProcParamType string //过程的参数类型
type TypeName string      //节点类型名，节点为声明类型时有效
type ExpVarKind string    //表达式的变量类型
type ExpType string       //表达是检查类型

const (
	ProK            NodeKind = "ProK"
	PheadK          NodeKind = "PheadK"
	TypeK           NodeKind = "TypeK"
	VarK            NodeKind = "VarK"
	ProcDecK        NodeKind = "ProcDecK"
	StmLK           NodeKind = "StmLK"
	DecK            NodeKind = "DecK"
	StmtK           NodeKind = "StmtK"
	ExpK            NodeKind = "ExpK"
	DefaultNodeKind NodeKind = ""

	ArrayK      Kind = "ArrayK"
	CharK       Kind = "CharK"
	IntegerK    Kind = "IntegerK"
	RecordK     Kind = "RecordK"
	IdK         Kind = "IdK"
	IfK         Kind = "IfK"
	WhileK      Kind = "WhileK"
	AssignK     Kind = "AssignK"
	ReadK       Kind = "ReadK"
	WriteK      Kind = "WriteK"
	CallK       Kind = "CallK"
	ReturnK     Kind = "ReturnK"
	OpK         Kind = "OpK"
	ConstK      Kind = "ConstK"
	DefaultKind Kind = ""

	ValParamType     ProcParamType = "valparam"
	VarParamType     ProcParamType = "varparam"
	DefaultParamType ProcParamType = ""

	IdV               ExpVarKind = "IdV"
	ArrayMembV        ExpVarKind = "ArrayMemebV"
	ParamMembV        ExpVarKind = "ParamMembV"
	FieldMembV        ExpVarKind = "FieldMembV"
	DefaultExpVarKind ExpVarKind = ""

	ExpInteger     ExpType = "Integer"
	ExpBoolean     ExpType = "Boolean"
	DefaultExpType ExpType = ""
)

type ArrayAttr struct {
	Low       int
	Top       int
	ChildType Kind
}

type ProcAttr struct {
	ParamType ProcParamType
}

type ExpAttr struct {
	Op      string
	Val     string
	VarKind ExpVarKind
	Type    ExpType
	Paren   bool //标记表达式节点是否包裹括号
}

type Attr struct {
	ArrayAttr *ArrayAttr
	ProcAttr  *ProcAttr
	ExpAttr   *ExpAttr
}

type TreeNode struct {
	IsAbstract bool
	Line       int
	NodeKind   NodeKind
	Kind       Kind
	IdNum      int
	Name       []string
	TypeName   string
	Children   []*TreeNode
	Attr       Attr
}

func NewTreeNode() *TreeNode {
	return &TreeNode{
		IsAbstract: false,
		Line:       0,
		NodeKind:   DefaultNodeKind,
		Kind:       DefaultKind,
		IdNum:      0,
		Name:       []string{},
		TypeName:   "",
		Children:   []*TreeNode{},
		Attr:       Attr{nil, nil, nil},
	}
}

func (node *TreeNode) ToString(prefix string) string {
	if node == nil {
		return ""
	}
	// fmt.Println(node)
	res := prefix
	res += string(node.NodeKind) + " "
	res += string(node.Kind) + " "
	for _, name := range node.Name {
		res += name + " "
	}
	if node.NodeKind == DecK && node.Kind == Kind(IdV) {
		res += node.TypeName + " "
	}
	res += node.Attr.ToString(node)
	for _, child := range node.Children {
		res += "\n" + child.ToString(prefix+"\t")
	}

	return res

	// if node.Attr.ProcAttr.ParamType != "" {
	// 	res += string(node.Attr.ProcAttr.ParamType) + " "
	// }

	// res += string(node.Kind) + " "
	// for _, id := range node.Name {
	// 	res += id + " "
	// }

	// if node.Kind == ArrayK {
	// 	res += strconv.Itoa(node.Attr.ArrayAttr.Low) + " "
	// 	res += strconv.Itoa(node.Attr.ArrayAttr.Top) + " "
	// 	res += string(node.Attr.ArrayAttr.ChildType) + " "
	// }
	// if node.NodeKind == ExpK {
	// 	if node.Kind == OpK {
	// 		res += node.Attr.ExpAttr.Op + " "
	// 	} else {
	// 		res += string(node.Attr.ExpAttr.VarKind) + " "
	// 		if node.Attr.ExpAttr.VarKind == ExpVarKind(ConstK) {
	// 			res += node.Attr.ExpAttr.Val
	// 		}
	// 	}

	// }

	// res += node.TypeName + " "

	// for _, child := range node.Children {
	// 	res += "\n" + child.ToString(prefix+"\t")
	// }

	// return res
}
func (attr *Attr) ToString(node *TreeNode) string {
	res := ""

	if attr.ArrayAttr != nil {
		res += strconv.Itoa(attr.ArrayAttr.Low) + " "
		res += strconv.Itoa(attr.ArrayAttr.Top) + " "
		res += string(attr.ArrayAttr.ChildType) + " "
	}
	if attr.ExpAttr != nil {
		if node.Kind == OpK {
			res += attr.ExpAttr.Op + " "
		}
		if node.Kind == ConstK {
			res += attr.ExpAttr.Val + " "
		}
		if node.Kind == IdK {
			res += string(attr.ExpAttr.VarKind) + " "
		}
	}
	if attr.ProcAttr != nil {
		res += string(attr.ProcAttr.ParamType) + " "
	}

	return res
}

func (node *TreeNode) ToProgram(prefix string, fa *TreeNode) string { //生成代码
	res := ""

	switch node.NodeKind {
	case ProK:
		for _, child := range node.Children {
			res += child.ToProgram(prefix, node) + "\n"
		}
		return res
	case PheadK:
		res += "program " + node.Name[0] + "\n"
		for _, child := range node.Children {
			res += child.ToProgram(prefix, node) + "\n"
		}
		return res
	case TypeK:
		res += "type\n"
		prefix += "\t"
	case VarK:
		res += "var\n"
		prefix += "\t"
	case ProcDecK:
	case StmLK:
		for i := 0; i < len(node.Children); i++ {
			res += node.Children[i].ToProgram(prefix, node)
			if i < len(node.Children)-1 {
				res += ";\n"
			}
		}
		return res
	case DecK:
		switch fa.NodeKind {
		case TypeK:
			switch node.Kind {
			case ArrayK:
			case CharK:
			case IntegerK:
			case RecordK:
			case IdK:
			}
		case VarK:
			switch node.Kind {
			case ArrayK:
			case CharK:
			case IntegerK:
			case RecordK:
			case IdK:
			}
		case ProcDecK:
			switch node.Kind {
			case ArrayK:
			case CharK:
			case IntegerK:
			case RecordK:
			case IdK:
			}
		}
	case StmtK:
		switch node.Kind {
		case IfK:
		case WhileK:
		case AssignK:
		case ReadK:
		case WriteK:
		case CallK:
		case ReturnK:
		}
	case ExpK:
		switch node.Kind {
		case OpK:
		case ConstK:
		case IdK:
		}
	}
	return res
}
