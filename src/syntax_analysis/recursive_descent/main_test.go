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

	node, err := statement.TypeDec()

	fmt.Println("error: ", err)

	fmt.Println(node.ToString(""))
}
