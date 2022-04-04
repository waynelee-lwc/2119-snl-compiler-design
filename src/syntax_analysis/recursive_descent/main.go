package main

import (
	"encoding/json"
	"fmt"
	"os"
	"recursive_descent_parser/model/statement"
	"recursive_descent_parser/model/token_set"
)

func main() {
	// fmt.Println("hello")
	// fmt.Println(os.Args)
	if len(os.Args) != 2 {
		fmt.Println("usage : ./runnable {programpath}")
		return
	}

	programName := os.Args[1]
	tkFile := fmt.Sprintf("%v/tk", programName)
	treeFile := fmt.Sprintf("%v/tree", programName)
	errorFile := fmt.Sprintf("%v/synerr", programName)
	geneFile := fmt.Sprintf("%v/gene", programName)

	tokens, _ := LoadTokens(tkFile)
	token_set.Initscanner(tokens)

	errList := []error{}
	program, err := statement.Program()
	errList = append(errList, err)

	tree := program.ToString("")
	gene := program.ToProgram("", nil)

	errList = append(errList, Save(treeFile, tree))
	errList = append(errList, Save(geneFile, gene))

	errs, _ := json.Marshal(errList)
	fmt.Println(os.Getwd())
	fmt.Println(Save(errorFile, string(errs)))
}
