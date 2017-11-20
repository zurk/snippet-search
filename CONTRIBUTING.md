# Architecture

This application is built with a frontend and a backend that can be ran &ndash;once you meet all the [dependencies](README.md#dependencies)&ndash; executing, from the root path:

```bash
make serve;
```
and then going to http://localhost:3001

The frontend and the backend can also be ran separately as it is explained below these lines.

## Frontend

It will let you upload any source code file to analyze it and view its snippets

Run it with the command:

```bash
make front-dependencies; # only needed the first time you use it, or you require new front dependencies.
cd web-ui && yarn start;
```

## Server

The server process the frontend request doing the following:

1. Calls `bblfsh` to get the identifiers in the passed source code,
2. Calls the `line_ids2graph` library to obtain the snippets and returns them.

Run it with the command:

```bash
make build-server; # only needed the first time you use it, or after you change the server go source code.
idex-server/bin/server;
```

It is not needed any other argument, it will use the default configuration

### Build the server

Whenever you ran `make serve` the server is recompiled automatically; if you change the server go sources, the application must be stopped and then run it again.

If you are serving the backend separately, or if you need to manually recompile the server, it can be done running:

```bash
make build-server;
```

# Fetch identifiers in sour code

The go server part can be used to retrieve the identifiers from a file as a command line tool. To do so, the server calls `bblfsh` and returns a json with all identifiers found and the lines where they were found.

```bash
make build-server; # only needed the first time you use it, or after you change the server go source code.
idex-server/bin/server -file <PATH_TO_SOURCE_CODE>;
```
