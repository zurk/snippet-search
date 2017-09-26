package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"log"

	"gopkg.in/bblfsh/client-go.v1"
	"gopkg.in/bblfsh/sdk.v1/uast"
)

var (
	serverAddr string
	filename   string
	language   string
	out        string
)

func main() {
	flag.StringVar(&serverAddr, "addr", ":9432", "bblfsh server endpoint")
	flag.StringVar(&filename, "file", "", "file to parse")
	flag.StringVar(&language, "lang", "", "source code language")
	flag.StringVar(&out, "out", "", "output")
	flag.Parse()

	bblfshClient, err := bblfsh.NewBblfshClient(serverAddr)
	if err != nil {
		log.Fatal(err)
	}

	content, err := ioutil.ReadFile(filename)
	if err != nil {
		log.Fatal(err)
	}

	res, err := bblfshClient.NewParseRequest().Language(language).Content(string(content)).Do()
	if err != nil {
		log.Fatal(err)
	}

	snippetNodes := map[string][]uint32{}
	iterateIdentifiers(res.UAST, snippetNodes)
	data, err := json.MarshalIndent(snippetNodes, "", "\t")
	if err != nil {
		log.Fatal(err)
	}

	if out != "" {
		if err := ioutil.WriteFile(out, data, 0755); err != nil {
			log.Fatal(err)
		}
	} else {
		fmt.Println(string(data))
	}
}

func iterateIdentifiers(u *uast.Node, snippetNodes map[string][]uint32) {
	for _, role := range u.Roles {
		if role == uast.Identifier {
			if u.Token != "" && u.StartPosition != nil {
				snippetNodes[u.Token] = append(snippetNodes[u.Token], u.StartPosition.Line)
			}
		}
	}

	for _, child := range u.Children {
		iterateIdentifiers(child, snippetNodes)
	}
}
