package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os/exec"

	bblfsh "gopkg.in/bblfsh/client-go.v2"
	"gopkg.in/bblfsh/sdk.v1/uast"
)

func parseHandler(w http.ResponseWriter, r *http.Request) {
	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		writeError(w, err, http.StatusBadRequest)
		return
	}

	source := &request{}
	if err := json.Unmarshal(body, source); err != nil {
		writeError(w, err, http.StatusBadRequest)
		return
	}

	if source.Content == "" {
		writeError(w, fmt.Errorf("Empty request"), http.StatusBadRequest)
		return
	}

	}

	identifiersAndLines, err := extractIdentifiers(source.Filename, source.Content)
	if err != nil {
		writeError(w, err, http.StatusInternalServerError)
		return
	}

	if len(identifiersAndLines) == 0 {
		writeError(w, fmt.Errorf("No identifiers found"), http.StatusInternalServerError)
		return
	}

	data, err := getGraph(identifiersAndLines)
	if err != nil {
		writeError(w, err, http.StatusInternalServerError)
		return
	}

	fmt.Fprint(w, string(data))
}

func extractIdentifiers(lang string, content string) (map[string][]uint32, error) {
	if lang == "" {
		lang = defaultLanguage
	}

	identifiersAndLines := map[string][]uint32{}

	bblfshClient, err := bblfsh.NewClient(bblfshAddr)
	if err != nil {
		return nil, err
	}

	res, err := bblfshClient.NewParseRequest().Language(lang).Content(content).Do()
	if err != nil {
		return nil, err
	}

	if res.UAST == nil {
		return nil, fmt.Errorf("Empty UAST")
	}

	iterateIdentifiers(res.UAST, identifiersAndLines)
	return identifiersAndLines, nil
}

func iterateIdentifiers(u *uast.Node, identifiersAndLines map[string][]uint32) {
	for _, role := range u.Roles {
		if role == uast.Identifier {
			if u.Token != "" && u.StartPosition != nil {
				identifiersAndLines[u.Token] = append(identifiersAndLines[u.Token], u.StartPosition.Line)
			}
		}
	}

	for _, child := range u.Children {
		iterateIdentifiers(child, identifiersAndLines)
	}
}

func getGraph(identifiersAndLines map[string][]uint32) ([]byte, error) {
	data, err := json.Marshal(identifiersAndLines)
	if err != nil {
		return nil, err
	}

	cmd := exec.Command("python3", pyScript)
	cmd.Stdin = bytes.NewReader(data)
	var out bytes.Buffer
	var outErr bytes.Buffer
	cmd.Stdout = &out
	cmd.Stderr = &outErr
	err = cmd.Run()
	if err != nil {
		return nil, fmt.Errorf(string(outErr.Bytes()))
	}

	return out.Bytes(), nil
}

func writeError(w http.ResponseWriter, err error, errCode int) {
	log.Println(err)
	http.Error(w, err.Error(), errCode)
}
