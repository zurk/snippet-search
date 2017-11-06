Snippet Search
====

## Run it
Run the server (without any other argument, it will use the default config)
```
./server
```

Run the frontend
```
cd public; yarn start
```

### dependencies
Some python libraries
```
sudo apt-get install libigraph0-dev
sudo pip3 install networkx==1.11
sudo pip3 install python-igraph
```

[bblfsh](https://doc.bblf.sh)
```
docker run -d --name bblfshd --privileged -p 9432:9432 bblfsh/bblfshd
docker exec -it bblfshd bblfshctl driver install --all
```

[Yarn](https://yarnpkg.com/lang/en/docs/install/)

## License

MIT, see [LICENSE](LICENSE)
