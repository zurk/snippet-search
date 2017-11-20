build:
	CGO_ENABLED=0 go build -o idex-server/bin/server idex-server/*.go

dependencies: front-dependencies build

front-dependencies:
	cd web-ui && yarn install

start: dependencies
	cd web-ui && node_modules/.bin/termax server
