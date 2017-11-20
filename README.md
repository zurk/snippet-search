Snippet Search
====

Project that guess _snippets_ inside source code

# Run it

It is needed to run the frontend and the server; once you meet all the [dependencies](README.md#dependencies), you can launch the application running:

```bash
make serve;
```
and go to http://localhost:3001

You can also run the server and the backend separately; you'll find more info about it in the [CONTRIBUTING.md](CONTRIBUTING.md)

# Dependencies

[Go installed](https://golang.org/doc/install#install), and the [`$GOPATH` properly configured](https://github.com/golang/go/wiki/SettingGOPATH); you can check if it's properly installed and configured obtaining a valid output for these commands:
```bash
go version; # prints your go version
echo $GOPATH; # prints your $GOPATH path
```

[Python3](https://www.python.org/download/releases/3.0/) and some python libraries, to find the snippets.
```bash
sudo apt-get install libigraph0-dev
sudo pip3 install networkx==1.11
sudo pip3 install python-igraph
```

[bblfsh](https://doc.bblf.sh) installed and locally running to find the identifiers.
```bash
docker run -d --name bblfshd --privileged -p 9432:9432 bblfsh/bblfshd
docker exec -it bblfshd bblfshctl driver install --all
```

[Yarn](https://yarnpkg.com/lang/en/docs/install/) to build and serve the frontend

# Contributing

If you want more info about the internals, project architecture or even you're interesting in contributing to this project, you will find more info in the [CONTRIBUTING.md](CONTRIBUTING.md).

# License

MIT, see [LICENSE](LICENSE)
