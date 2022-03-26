package tree_node

type NodeKind string      //语法树节点类型
type Kind string          //语法树节点具体类型
type ProcParamType string //过程的参数类型
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

	ValParamType     ProcParamType = "valparamtype"
	VarParamType     ProcParamType = "varparamtype"
	DefaultParamType ProcParamType = ""

	IdV               ExpVarKind = "IdV"
	ArrayMembV        ExpVarKind = "ArrayMemebV"
	ParamMembV        ExpVarKind = "ParamMembV"
	DefaultExpVarKind ExpVarKind = ""

	ExpInteger     ExpType = "Integer"
	ExpBoolean     ExpType = "Boolean"
	DefaultExpType ExpType = ""
)

type ArrayAttr struct {
	Low       int
	High      int
	ChildType string
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
