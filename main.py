#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import yaml
import os.path

yamlFilePath = "example-config.yaml"

if os.path.isfile("config.yml"):
    yamlFilePath = "config.yml"

if os.path.isfile("config.yaml"):
    yamlFilePath = "config.yaml"

with open(yamlFilePath, 'r') as f:
    config = yaml.load(f)
# print(config)
# for route in config:
#     print(config[route])
#     print(config[route]["from"])
#     print(config[route]["to"])
#     print(config[route]["region"])


class HTTPServer_RequestHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client
        message = "Hello world!"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return


def startServer():
    print('starting server...')

    # Server settings
    # Choose port 8081, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


startServer()