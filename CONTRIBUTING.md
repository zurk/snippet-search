# Architecture

The frontend and the backend can be ran separately

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

If you need to recompile the server, you can do it running:

```bash
make build
```
