# Architecture

This application is built with a frontend and a backend that can be ran &ndash;once you meet all the [dependencies](README.md#dependencies)&ndash; executing, from the root path:

```bash
make start;
```
and then going to http://localhost:3001

The frontend and the backend can also be ran separately as it is explained below these lines.

## Frontend

It will let you upload any source code file to analyze it and view its snippets

Run it with the command:

```bash
cd web-ui && yarn install && yarn start;
```

## Server

The server process the frontend request doing the following:

1. Calls `bblfsh` to get the identifiers in the passed source code,
2. Calls the `line_ids2graph` library to obtain the snippets and returns them.

Run it with the command:

```bash
idex-server/bin/server;
```

It is not needed any other argument, it will use the default configuration

### Build the server

Whenever you ran `make start` the server is recompiled automatically; if you change the server go sources, the application must be stopped and then run it again.

If you are serving the backend separately, or if you need to manually recompile the server, it can be done running:

```bash
make build
```
