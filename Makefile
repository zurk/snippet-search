build-server: server-dependencies
	CGO_ENABLED=0 go build -o idex-server/bin/server idex-server/*.go

server-dependencies:
	go get ./...

build-front: front-dependencies
	cd web-ui && yarn build

front-dependencies:
	cd web-ui && yarn install

dependencies: server-dependencies front-dependencies

build: build-server build-front

serve: build-server front-dependencies
	cd web-ui && node_modules/.bin/termax server
