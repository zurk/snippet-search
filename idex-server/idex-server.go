package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"

	"github.com/gorilla/handlers"
	"github.com/gorilla/mux"
)

var (
	filePath        string
	addr            string
	bblfshAddr      string
	defaultLanguage string
	pyScript        string
)

type request struct {
	Filename string
	Language string
	Content  string
}

func main() {
	flag.StringVar(&filePath, "file", "", "Path to source code to analyze. If it's set, it will output the identifiers found.")
	flag.StringVar(&addr, "addr", ":8080", "endpoint to bind")
	flag.StringVar(&bblfshAddr, "bblfsh", ":9432", "bblfsh server endpoint")
	flag.StringVar(&defaultLanguage, "lang", "python", "file language")
	flag.StringVar(&pyScript, "script", "line_ids2graph.py", "script to generate graph")
	flag.Parse()

	if filePath == "" {
		router := mux.NewRouter()
		router.Handle("/parse", handlers.CombinedLoggingHandler(os.Stdout, http.HandlerFunc(parseHandler))).Methods(http.MethodPost)
		log.Fatal(http.ListenAndServe(addr, router))
	} else {
		printIdentifiers(filePath)
	}
}

func printIdentifiers(path string) {
	sourceCode, err := ioutil.ReadFile(filePath)
	if err != nil {
		log.Fatal(err)
	}

	identifiers, err := extractIdentifiers(filePath, string(sourceCode))
	if err != nil {
		log.Fatal(err)
	}

	data, err := json.MarshalIndent(identifiers, "", "\t")
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(string(data))
}
