package main

import (
	"flag"
	"log"
	"net/http"
	"os"

	"github.com/gorilla/handlers"
	"github.com/gorilla/mux"
)

var (
	addr            string
	bblfshAddr      string
	defaultLanguage string
	pyScript        string
)

type request struct {
	Filename string `json:"omitempty"`
	Language string `json:"omitempty"`
	Content  string
}

func main() {
	flag.StringVar(&addr, "addr", ":8080", "endpoint to bind")
	flag.StringVar(&bblfshAddr, "bblfsh", ":9432", "bblfsh server endpoint")
	flag.StringVar(&defaultLanguage, "lang", "python", "file language")
	flag.StringVar(&pyScript, "script", "line_ids2graph.py", "script to generate graph")
	flag.Parse()

	router := mux.NewRouter()
	router.Handle("/parse", handlers.CombinedLoggingHandler(os.Stdout, http.HandlerFunc(parseHandler))).Methods(http.MethodPost)
	log.Fatal(http.ListenAndServe(addr, router))
}
