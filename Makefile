.venv:
	python3 -m venv .venv

python-lint:
	black --check server.py
	flake8 server.py

python-install: .venv
	.venv/bin/python3 -m pip install -r requirements.txt

protostubs:
	protoc -I=. helloworld.proto --js_out=import_style=commonjs:. --grpc-web_out=import_style=commonjs,mode=grpcwebtext:.
	PATH=.venv/bin .venv/bin/python3 -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. --mypy_out=. --mypy_grpc_out=. helloworld.proto

webpack:
	npx webpack client.js

all: protostubs webpack

install: python-install
