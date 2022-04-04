package main

import (
	"encoding/json"
	"os"
	"recursive_descent_parser/model/token"
)

//读取token序列
func LoadTokens(file string) ([]*token.Token, error) {
	tokens := []*token.Token{}
	program, err := os.ReadFile(file)
	if err != nil {
		return nil, err
	}
	if err = json.Unmarshal(program, &tokens); err != nil {
		return tokens, err
	}
	return tokens, err
}

func Save(filePath string, tree string) error {
	file, err := os.Create(filePath)
	if err != nil {
		return err
	}
	defer file.Close()
	_, err = file.WriteString(tree)
	return err

}
