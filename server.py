from flask import Flask, send_from_directory
from sonora.wsgi import grpcWSGI

import helloworld_pb2
import helloworld_pb2_grpc

FORMAT_STRING = "Hello, {request.name}"

app = Flask(__name__)


class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        print(f"We are saying hello to {request.name}")
        return helloworld_pb2.HelloReply(message=FORMAT_STRING.format(request=request))

    def SayRepeatHello(self, request, context):
        return helloworld_pb2.HelloReply(
            message=FORMAT_STRING.format(request=request) * request.count
        )


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/<path:path>")
def foo(path):
    if path == "/":
        path = "index.html"
    # This appears to filter ../ for us.
    return send_from_directory(".", path)


if __name__ == "__main__":
    app.wsgi_app = grpcWSGI(app.wsgi_app)
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), app.wsgi_app)
    app.run()
