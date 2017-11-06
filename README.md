Snippet Search
====

Project that guess _snippets_ inside source code

# Run it

It is needed to run the frontend and the server; you can do so running:

```bash
make start;
```
and go to http://localhost:3001

You can also run the server and the backend separately; you'll find more info about it in the [CONTRIBUTING.md](CONTRIBUTING.md)

# Dependencies

[Python3](https://www.python.org/download/releases/3.0/) and some python libraries, to find the snippets.
```bash
sudo apt-get install libigraph0-dev
sudo pip3 install networkx==1.11
sudo pip3 install python-igraph
```

[bblfsh](https://doc.bblf.sh) to find the identifiers.
```bash
docker run -d --name bblfshd --privileged -p 9432:9432 bblfsh/bblfshd
docker exec -it bblfshd bblfshctl driver install --all
```

[Yarn](https://yarnpkg.com/lang/en/docs/install/) to run and build the frontend

# Contributing

If you want more info about the internals, project architecture or even you're interesting in contributing to this project, you will find more info in the [CONTRIBUTING.md](CONTRIBUTING.md).

# License

MIT, see [LICENSE](LICENSE)
