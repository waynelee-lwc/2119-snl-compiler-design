package main

import (
	"fmt"
	"recursive_descent_parser/model/statement"
	"recursive_descent_parser/model/token"
	"recursive_descent_parser/model/token_set"
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
	tokens, _ := LoadTokens("../../../outputs/test_output_tokens1.txt")
	token_set.Initscanner(tokens)

	// typeNode, _ := statement.TypeDec()
	// varNode, _ := statement.VarDec()
	// procedureNodes, err := statement.ProcDec()

	// fmt.Println("error: ", err)

	// fmt.Println(typeNode.ToString(""))
	// fmt.Println(varNode.ToString(""))
	// for _, procdure := range procedureNodes {
	// 	fmt.Println(procdure.ToString(""))
	// }
	program, _ := statement.Program()

	fmt.Println(program.ToString(""))
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
procedure q(var char name;integer age)
begin
end

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
