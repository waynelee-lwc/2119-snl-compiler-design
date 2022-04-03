package main

import (
	"fmt"
	"recursive_descent_parser/model/statement"
	"recursive_descent_parser/model/token"
	"recursive_descent_parser/model/token_set"
	"recursive_descent_parser/model/tree_node"
	"testing"
)

func TestMain(t *testing.T) {
	tokens, err := LoadTokens("../../../outputs/test_output_tokens1.txt")
	fmt.Println(err)
	for _, token := range tokens {
		fmt.Println(token)
	}
}

func TestPredict(t *testing.T) {
	Program := &token.Token{
		Type: token.Reserved,
		Name: "program",
	}
	Colon := &token.Token{
		Type: token.Seperator,
		Name: ":",
	}
	Semi := &token.Token{
		Type: token.Seperator,
		Name: ";",
	}
	fmt.Println(token_set.DemoPredict.Predict(Program))
	fmt.Println(token_set.DemoPredict.Predict(Colon))
	fmt.Println(token_set.DemoPredict.Predict(Semi))
}

func TestTokenReader(t *testing.T) {
	// tokenList := &[]*token.Token{
	// 	{
	// 		Type: token.Number,
	// 		Name: "10",
	// 	},
	// 	{
	// 		Type: token.Number,
	// 		Name: "9",
	// 	},
	// 	{
	// 		Type: token.Number,
	// 		Name: "8",
	// 	},
	// 	{
	// 		Type: token.Number,
	// 		Name: "7",
	// 	},
	// }
	tokenList, _ := LoadTokens("../../../outputs/test_output_tokens.txt")

	token_set.Initscanner(tokenList)

	for token_set.Scanner.HasNext() {
		fmt.Println(token_set.Scanner.Poll())
	}
}

func TestTypeDec(t *testing.T) {
	tokens, _ := LoadTokens("../../../outputs/bubble_sort.tk")
	token_set.Initscanner(tokens)
	for _, token := range tokens {
		fmt.Println(token)
	}

	// typeNode, _ := statement.TypeDec()
	// varNode, _ := statement.VarDec()
	// procedureNodes, err := statement.ProcDec()

	// fmt.Println("error: ", err)

	// fmt.Println(typeNode.ToString(""))
	// fmt.Println(varNode.ToString(""))
	// for _, procdure := range procedureNodes {
	// 	fmt.Println(procdure.ToString(""))
	// }
	program, err := statement.Program()

	fmt.Println("error ", err)
	// fmt.Println(program.ToString(""))
	err = SaveSyntaxTree("../../../outputs/bubble_sort.tree", program.ToString(""))
	fmt.Println("error ", err)
	fmt.Println(program.ToProgram("", nil))
	generated := program.ToProgram("", nil)
	err = SaveSyntaxTree("../../../outputs/bubble_sort.gene", generated)
	fmt.Println(err)
}

func TestCreateNameList(t *testing.T) {
	nameList := []string{"a", "b", "hello", "world"}
	fmt.Println(tree_node.CreateNameList(nameList))
	// fmt.Println(fmt.Sprintf("hello %v", "wayne"))
}

func TestGeneProgram(t *testing.T) {

	//定义节点1
	decNodeParam1 := tree_node.NewTreeNode()
	decNodeParam1.Attr.ProcAttr = &tree_node.ProcAttr{
		ParamType: tree_node.ValParamType,
	}
	decNodeParam1.Name = append(decNodeParam1.Name, "a", "b")
	decNodeParam1.NodeKind = tree_node.DecK
	decNodeParam1.Kind = tree_node.IntegerK
	//定义节点2
	decNodeParam2 := tree_node.NewTreeNode()
	decNodeParam2.NodeKind = tree_node.DecK
	decNodeParam2.Kind = tree_node.ArrayK
	decNodeParam2.Attr.ArrayAttr = &tree_node.ArrayAttr{
		Low:       0,
		Top:       30,
		ChildType: tree_node.ChildTypeChar,
	}
	decNodeParam2.Name = append(decNodeParam2.Name, "c", "d")
	decNodeParam2.Attr.ProcAttr = &tree_node.ProcAttr{
		ParamType: tree_node.VarParamType,
	}
	//定义节点3
	decNodeParam3 := tree_node.NewTreeNode()
	decNodeParam3.NodeKind = tree_node.DecK
	decNodeParam3.Kind = tree_node.IdK
	decNodeParam3.TypeName = "t1"
	decNodeParam3.Name = append(decNodeParam3.Name, "e")
	decNodeParam3.Attr.ProcAttr = &tree_node.ProcAttr{
		ParamType: tree_node.ValParamType,
	}
	//定义节点4
	decNodeParam4 := tree_node.NewTreeNode()
	decNodeParam4.NodeKind = tree_node.DecK
	decNodeParam4.Kind = tree_node.RecordK
	decNodeParam4.Name = append(decNodeParam4.Name, "v1", "v2")
	decNodeParam4.Attr.ProcAttr = &tree_node.ProcAttr{
		ParamType: tree_node.VarParamType,
	}
	decNodeParam4.Children = append(decNodeParam4.Children, decNodeParam1, decNodeParam2)

	//类型节点
	typeNode := tree_node.NewTreeNode()
	typeNode.NodeKind = tree_node.TypeK
	typeNode.Children = append(typeNode.Children, decNodeParam1, decNodeParam2, decNodeParam3, decNodeParam4)
	// fmt.Println(typeNode.ToProgram("", nil))

	//变量节点
	varNode := tree_node.NewTreeNode()
	varNode.NodeKind = tree_node.VarK
	varNode.Children = append(varNode.Children, decNodeParam1, decNodeParam2, decNodeParam3, decNodeParam4)
	// fmt.Println(varNode.ToProgram("", nil))

	//过程定义节点
	procDecNode := tree_node.NewTreeNode()
	procDecNode.NodeKind = tree_node.ProcDecK
	procDecNode.Name = append(procDecNode.Name, "proc")
	procDecNode.Children = append(procDecNode.Children, decNodeParam1, decNodeParam2, decNodeParam3, decNodeParam4)
	procDecNode.Children = append(procDecNode.Children, typeNode, varNode)
	// fmt.Println(procDecNode.ToProgram("", nil))

	//程序头节点
	headNode := tree_node.NewTreeNode()
	headNode.NodeKind = tree_node.PheadK
	headNode.Name = append(headNode.Name, "testP")
	headNode.Children = append(headNode.Children, typeNode, varNode, procDecNode)
	fmt.Print(headNode.ToProgram("", nil))
}

/*
program p
type
	t1 = integer;
	t2 = array[1..20] of integer;
	t3 = char;
	t4 = record
		integer a,b;
		char c,d;
		array[1..30]of char e,f;
		end;
	t5 = t1
var
	t1 v1;
	t2 v2;
	t3 v3;
	t4 v4;
	t5 v5;
	integer a,b;
	char c,d;
	array[1..20]of integer e,f;
	record
		integer a;
		char b;
		end g,h;
procedure p(integer a,b;char c,d;var t1 v1;record integer a,b; end r1)
	type
		t1 = integer;
	var
		t1 v1,v2;
	begin
		read(v1);
		v2 = v1+1;
		write(v2);
	end
procedure q(var char name;integer age)
	type
		Person = record
			integer age;
			char name;
			end;
	var
		Person person;
	begin
		person.name = name;
		person.age = age;
		write(person.name);
		return;
	end
begin
	read(c)
	read(a)
	q(c,a)
end.

TypeK
	DecK IntegerK t1
	DecK ArrayK t2 1 20 IntegerK
	DecK CharK t3
	DecK RecordK t4
		Deck IntegerK a b
		DecK CharK c d
		DecK ArrayK e f 1 30 CharK
	DecK IdK t1 t5
VarK
	DecK IdK t1 v1
	DecK IdK t2 v2
	DecK IdK t3 v3
	DecK IdK t4 v4
	DecK IdK t5 v5
	DecK IntegerK a b
	DecK CharK c d
	DecK ArrayK e f
	DecK RecordK g,h
		DecK IntegerK a
		DecK CharK b
ProcDecK p
	DecK valparam IntegerK a,b
	DecK valparam CharK c,d
	DecK varparam IdK t1 v1
	DecK valparam RecordK r1
		Deck IntegerK a,b
ProcDecK q
	DecK varparam CharK name
	DecK valparam Integer age


*/
