package tree_node

import (
	"encoding/json"
	"fmt"
	"strconv"
)

type NodeKind string      //语法树节点类型
type Kind string          //语法树节点具体类型
type ProcParamType string //过程的参数类型
type TypeName string      //节点类型名，节点为声明类型时有效
type ExpVarKind string    //表达式的变量类型
type ExpType string       //表达是检查类型
type ChildType string     //数组子节点类型

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

	ChildTypeChar    ChildType = "CharK"
	ChildTypeInteger ChildType = "IntegerK"

	Indentation = "\t"
)

var BaseType2ChildType = map[Kind]ChildType{
	CharK:    ChildTypeChar,
	IntegerK: ChildTypeInteger,
}

var LNeedParan = map[string]bool{
	"++": false,
	"+-": false,
	"+*": false,
	"+/": false,
	"-+": false,
	"--": false,
	"-*": false,
	"-/": false,
	"*+": true,
	"*-": true,
	"**": false,
	"*/": false,
	"/+": true,
	"/-": true,
	"/*": false,
	"//": false,
}

var RNeedParan = map[string]bool{
	"++": false,
	"+-": false,
	"+*": false,
	"+/": false,
	"-+": true,
	"--": true,
	"-*": false,
	"-/": false,
	"*+": true,
	"*-": true,
	"**": false,
	"*/": false,
	"/+": true,
	"/-": true,
	"/*": true,
	"//": true,
}

type ArrayAttr struct {
	Low       int
	Top       int
	ChildType ChildType
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
	if node.NodeKind == DecK && node.Kind == IdK {
		res += node.TypeName + " "
	}
	for _, name := range node.Name {
		res += name + " "
	}
	res += node.Attr.ToString(node)
	for _, child := range node.Children {
		res += "\n" + child.ToString(prefix+Indentation)
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
	// 	res += "\n" + child.ToString(prefix+Indentation)
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

func (node *TreeNode) ToJSON(prefix string) string {
	res := prefix

	children := node.Children
	node.Children = nil
	str, _ := json.Marshal(node)

	res += string(str)
	for _, child := range children {
		res += "\n" + child.ToJSON(prefix+Indentation)
	}

	return res
}

func CreateNameList(list []string) string {
	res := ""

	for idx, name := range list {
		res += name
		if idx != len(list)-1 {
			res += ", "
		}
	}

	return res
}

func (node *TreeNode) ToProgram(prefix string, fa *TreeNode) string { //生成代码
	if node == nil {
		return ""
	}
	res := prefix

	switch node.NodeKind {
	case ProK: //程序跟节点
		for idx, child := range node.Children {
			res += child.ToProgram(prefix, node)
			if idx != len(node.Children)-1 {
				res += "\n"
			}
		}
		res += "."
	case PheadK: //程序头节点
		res += "program " + node.Name[0]
		// for _, child := range node.Children {
		// 	res += child.ToProgram(prefix, node) + "\n"
		// }
	case TypeK: //类型定义节点
		res += "type"
		prefix += Indentation
		for _, child := range node.Children {
			res += fmt.Sprintf("\n%v", child.ToProgram(prefix, node))
		}
	case VarK: //变量定义节点
		res += "var"
		prefix += Indentation
		for _, child := range node.Children {
			res += fmt.Sprintf("\n%v", child.ToProgram(prefix, node))
		}
	case ProcDecK: //过程定义节点
		res += "procedure " + node.Name[0] + "("
		for idx, child := range node.Children {
			if child.NodeKind == DecK {
				res += child.ToProgram("", node)
				if idx+1 < len(node.Children) && node.Children[idx+1].NodeKind == DecK {
					res += "; "
				} else {
					res += ");"
				}
			} else {
				res += "\n" + child.ToProgram(prefix+Indentation, node)
			}
		}
	case StmLK: //语句列表节点
		res += "begin"
		for idx, child := range node.Children {
			res += "\n" + child.ToProgram(prefix+Indentation, node)
			if idx != len(node.Children)-1 {
				res += ";"
			}
		}
		res += fmt.Sprintf("\n%vend", prefix)
	case DecK: //定义节点
		switch fa.NodeKind {
		case TypeK: //类型定义节点
			switch node.Kind {
			case ArrayK: //类型定义数组节点
				attr := node.Attr.ArrayAttr
				res += fmt.Sprintf("%v = array[%v..%v]of %v;", CreateNameList(node.Name), attr.Low, attr.Top, attr.ChildType)
			case CharK: //类型定义字符节点
				res += fmt.Sprintf("%v = char;", CreateNameList(node.Name))
			case IntegerK: //类型定义整型节点
				res += fmt.Sprintf("%v = integer;", CreateNameList(node.Name))
			case RecordK: //类型定义记录节点
				res += fmt.Sprintf("%v = record\n", CreateNameList(node.Name))
				prefix += Indentation
				for _, child := range node.Children {
					res += child.ToProgram(prefix, node) + "\n"
				}
				res += prefix[:len(prefix)-1] + "end;"
			case IdK: //类型定义类型节点
				res += fmt.Sprintf("%v = %v;", CreateNameList(node.Name), node.TypeName)
			}
		case VarK, DecK, ProcDecK: //变量定义 ｜ 记录定义 ｜ 过程参数定义 节点
			if fa.NodeKind == ProcDecK && node.Attr.ProcAttr.ParamType == VarParamType {
				//过程定义节点中需要处理变量和常量定义
				res += "var "
			}
			switch node.Kind {
			case ArrayK:
				attr := node.Attr.ArrayAttr
				res += fmt.Sprintf("array[%v..%v]of %v %v", attr.Low, attr.Top, attr.ChildType, CreateNameList(node.Name))
			case CharK:
				res += fmt.Sprintf("char %v", CreateNameList(node.Name))
			case IntegerK:
				res += fmt.Sprintf("integer %v", CreateNameList(node.Name))
			case RecordK:
				res += "record"
				if fa.NodeKind != ProcDecK {
					prefix += Indentation
					res += "\n"
				} else {
					prefix = " "
				}
				for _, child := range node.Children {
					res += child.ToProgram(prefix, node)
					if fa.NodeKind != ProcDecK {
						res += "\n"
					}
				}
				res += fmt.Sprintf("%vend %v", prefix[:len(prefix)-1], CreateNameList(node.Name))
			case IdK:
				res += fmt.Sprintf("%v %v", node.TypeName, CreateNameList(node.Name))
			}
			if fa.NodeKind != ProcDecK {
				//非过程参数定义节点，句末加上分号
				res += ";"
			}
		}
	case StmtK: //语句节点
		switch node.Kind {
		case IfK: //if语句
			res += fmt.Sprintf("if %v then", node.Children[0].ToProgram("", node))
			for i := 1; i < node.IdNum+1; i++ {
				res += "\n" + node.Children[i].ToProgram(prefix+Indentation, node)
				if i != node.IdNum {
					res += ";"
				}
			}
			if node.IdNum+1 < len(node.Children) {
				res += fmt.Sprintf("\n%velse", prefix)
				for i := node.IdNum + 1; i < len(node.Children); i++ {
					res += "\n" + node.Children[i].ToProgram(prefix+Indentation, node)
					if i != len(node.Children)-1 {
						res += ";"
					}
				}
			}
			res += fmt.Sprintf("\n%vfi", prefix)
		case WhileK: //while语句
			res += fmt.Sprintf("while %v do", node.Children[0].ToProgram("", node))
			for idx, child := range node.Children {
				if idx == 0 {
					continue
				}
				res += "\n" + child.ToProgram(prefix+Indentation, node)
				if idx != len(node.Children)-1 {
					res += ";"
				}
			}
			res += fmt.Sprintf("\n%vendwh", prefix)
		case AssignK: //赋值语句
			res += fmt.Sprintf("%v := %v", node.Children[0].ToProgram("", node), node.Children[1].ToProgram("", node))
		case ReadK: //读入语句
			res += fmt.Sprintf("read(%v)", CreateNameList(node.Name))
		case WriteK: //写出语句
			res += fmt.Sprintf("write(%v)", node.Children[0].ToProgram("", node))
		case CallK: //调用语句
			params := ""
			for idx, child := range node.Children {
				if idx == 0 {
					continue
				}
				params += child.ToProgram("", node)
				if idx != len(node.Children)-1 {
					params += ", "
				}
			}
			res += fmt.Sprintf("%v(%v)", node.Children[0].ToProgram("", node), params)
		case ReturnK:
		}
	case ExpK: //表达式节点
		switch node.Kind {
		case OpK: //符号节点
			lson := node.Children[0]
			rson := node.Children[1]
			l := ""
			r := ""
			if lSonNeedParan(node, lson) {
				l = fmt.Sprintf("(%v)", lson.ToProgram("", node))
			} else {
				l = lson.ToProgram("", node)
			}
			if rSonNeedParan(node, rson) {
				r = fmt.Sprintf("(%v)", rson.ToProgram("", node))
			} else {
				r = rson.ToProgram("", node)
			}
			attr := node.Attr.ExpAttr
			res += fmt.Sprintf("%v%v%v", l, attr.Op, r)
		case ConstK: //常量节点
			res = node.Attr.ExpAttr.Val
		case IdK: //变量节点
			attr := node.Attr.ExpAttr
			switch attr.VarKind {
			case IdV: //普通变量
				res += node.Name[0]
			case ArrayMembV: //数组类型变量
				res += fmt.Sprintf("%v[%v]", node.Name[0], node.Children[0].ToProgram("", node))
			case FieldMembV: //记录类型变量
				res += fmt.Sprintf("%v.%v", node.Name[0], node.Children[0].ToProgram("", node))
			}
		}
	}
	// fmt.Println(res)
	return res
}

//左符号是否需要括号
func lSonNeedParan(node *TreeNode, lson *TreeNode) bool {
	return lson.Kind == OpK && LNeedParan[node.Attr.ExpAttr.Op+lson.Attr.ExpAttr.Op]
}

//右符号是否需要括号
func rSonNeedParan(node *TreeNode, rson *TreeNode) bool {
	return rson.Kind == OpK && RNeedParan[node.Attr.ExpAttr.Op+rson.Attr.ExpAttr.Op]
}

/**
语句生成规则：
	Prok -> children
	PheadK {name} -> program {name} \n + children
	TypeK -> type \n + '\t'children
	VarK -> var \n + '\t'children
	ProcDecK {name} -> procedure {name}( childrenDecK );
	StmLK -> children
	DecK ArrayK {names} {{low} {top} {childType}}	-> array[{low}..{top}]of {childType} {names}; 	|VarK|
													-> {names} = array[{low}..{top}]of {childType}; |TypeK|
	DecK CharK {names}	-> char {names}; 	|VarK|
						-> {names} = char;	|TypeK|
	DecK IntegerK {names}	-> integer {names};		|VarK|
							-> {names} = integer;	|TypeK|
	DecK RecordK {names}	-> record \n + '\t'children \n end {names};		|VarK|
							-> {names} = record\n + '\t'children \n end;	|TypeK|
	DecK IdK {names} {typeName} -> {typeName} {names};	|VarK|
								-> {names} = {typeName};|TypeK|
	StmtK IfK
	StmtK WhileK
	StmtK AssignK
	StmtK ReadK {names}
	StmtK WriteK {names}
	StmtK CallK
	StmtK ReturnK
	ExpK OpK {{op}}
	ExpK ConstK {{val}}
	ExpK IdK {name} IdV
	ExpK IdK {name} ArrayMemebV
	ExpK IdK {name} FieldMemebV

*/
