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
	Val     int
	VarKind ExpVarKind
	Type    ExpType
}

type Attr struct {
	ArrayAttr ArrayAttr
	ProcAttr  ProcAttr
	ExpAttr   ExpAttr
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
		Attr:       Attr{},
	}
}

func (node *TreeNode) ToString(prefix string) string {
	if node == nil {
		return ""
	}
	// fmt.Println(node)
	res := prefix
	res += string(node.NodeKind) + " "

	if node.Attr.ProcAttr.ParamType != "" {
		res += string(node.Attr.ProcAttr.ParamType) + " "
	}

	res += string(node.Kind) + " "
	for _, id := range node.Name {
		res += id + " "
	}

	if node.Kind == ArrayK {
		res += strconv.Itoa(node.Attr.ArrayAttr.Low) + " "
		res += strconv.Itoa(node.Attr.ArrayAttr.Top) + " "
		res += string(node.Attr.ArrayAttr.ChildType) + " "
	}
	if node.NodeKind == ExpK {
		if node.Kind == OpK {
			res += node.Attr.ExpAttr.Op + " "
		} else {
			res += string(node.Attr.ExpAttr.VarKind) + " "
			if node.Attr.ExpAttr.VarKind == ExpVarKind(ConstK) {
				res += strconv.Itoa(node.Attr.ExpAttr.Val) + " "
			}
		}

	}

	res += node.TypeName + " "

	for _, child := range node.Children {
		res += "\n" + child.ToString(prefix+"\t")
	}

	return res
}
