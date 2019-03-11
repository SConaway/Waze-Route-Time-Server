#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import WazeRouteCalculator
import yaml
import os.path
import time
import logging

log = logging.getLogger(__name__)
log_lvl = logging.INFO
try:
    log.setLevel(log_lvl)
except NameError:
    log_lvl = logging.WARNING
    log.setLevel(log_lvl)


yamlFilePath = "example-config.yaml"

if os.path.isfile("config.yml"):
    yamlFilePath = "config.yml"

if os.path.isfile("config.yaml"):
    yamlFilePath = "config.yaml"
log.info("Config File: %s", yamlFilePath)
message = '{"message": "Check back later. Server is still starting."}'


def getTime(from_address, to_address, region):
    route = WazeRouteCalculator.WazeRouteCalculator(
        from_address, to_address, region, log_lvl=None)
    try:
        results = route.calc_route_info()
    except WazeRouteCalculator.WRCError as err:
        log.info("Sleeping for 10 seconds due to error: " + str(err))
        time.sleep(10)
        results = getTime(from_address, to_address, region)
    return(round(results[0], 2), round(results[1], 2))


def getTimes():
    log.info("Getting Times")
    with open(yamlFilePath, 'r') as f:
        config = yaml.load(f)
    log.info(config)
    for route in config:
        log.info(config[route])
        print(getTime(config[route]["from"], config[route]
                      ["to"], config[route]["region"]))
    return "hello"


def formatMessage(times):
    return times


class HTTPServer_RequestHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Send message back to client
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return


def startServer():
    log.info('starting server...')

    # Server settings
    # Choose port 8081, for port 80, which is normally used for
    # a http server, you need root access
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
    log.info('running server...')
    httpd.serve_forever()


formatMessage(getTimes)
threading.Timer(5.0, formatMessage(getTimes)).start()


if "TRAVIS" not in os.environ:
    pass
    startServer()
