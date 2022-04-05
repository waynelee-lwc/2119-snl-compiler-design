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

	errList := []string{}
	program, err := statement.Program()
	if err != nil {
		errList = append(errList, err.Error())
	} else {
		errList = append(errList, "")
	}
	// fmt.Println(err)

	tree := program.ToString("")
	gene := program.ToProgram("", nil)

	if err := Save(treeFile, tree); err != nil {
		errList = append(errList, err.Error())
	} else {
		errList = append(errList, "")
	}
	if err := Save(geneFile, gene); err != nil {
		errList = append(errList, err.Error())
	} else {
		errList = append(errList, "")
	}
	// fmt.Println(errList)
	errs, err := json.Marshal(errList)
	fmt.Println(string(errs), err)
	// fmt.Println(os.Getwd())
	fmt.Println(Save(errorFile, string(errs)))
}
