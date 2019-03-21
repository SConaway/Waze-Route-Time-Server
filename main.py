#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import json
import logging
import os.path
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

import WazeRouteCalculator
import yaml

logLevel = logging.DEBUG
logging.basicConfig(level=logLevel)

yamlFilePath = "example-config.yaml"
if os.path.isfile("config.yml"):
    yamlFilePath = "config.yml"
if os.path.isfile("config.yaml"):
    yamlFilePath = "config.yaml"
logging.info("Config File: %s", yamlFilePath)


class Message():
    def __init__(self):
        self.message = '{"message": "Check back later. Server is still starting."}'

    def update(self, m):
        self.message = m


class Route():
    def __init__(self, f, t, re):
        self.from_address = f
        self.to_address = t
        self.region = re
        self.color = "default"
        if self.region == "US" or self.region == "NA":
            self.units = "mi"
        else:
            self.units = "km"
        self.r = WazeRouteCalculator.WazeRouteCalculator(
            self.from_address, self.to_address, self.region, log_lvl=logLevel)

    def get_info(self):
        try:
            results = self.r.calc_route_info()
        except WazeRouteCalculator.WRCError as err:
            logging.info("Sleeping for 10 seconds due to error: " + str(err))
            time.sleep(10)
            results = get_info(self.from_address, self.to_address, self.region)
        return (round(results[0], 2), round(results[1], 2),
                self.units, self.color)


class HTTPServer_RequestHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Send message back to client as utf-8 data
        self.wfile.write(bytes(ms.message, "utf8"))
        return


def get_info(from_address, to_address, region):
    r = Route(from_address, to_address, region)
    return r.get_info()


def refresh():
    logging.info("Getting Times")
    # print("hi")
    with open(yamlFilePath, 'r') as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            logging.error("Error in configuration file: ", exc)
    logging.info(config)
    data = {}
    # data['key'] = 'value'
    json_data = json.dumps(data)
    i = 0
    for route in config:
        i = i + 1
        logging.info(config[route])
        routeTime, routeDist, routeUnits, routeColor = get_info(
            config[route]["from"],
            config[route]["to"],
            config[route]["region"])
        logging.info("Time: %s minutes, Distance: %s %s",
                     routeTime, routeDist, routeUnits)
        str = {}
        str['name'] = config[route]["name"]
        str['time'] = routeTime
        str['dist'] = routeDist
        str['units'] = routeUnits
        str['color'] = routeColor
        data[i] = str
        time.sleep(1)
    # TODO: this
    # data['lastUpdatedTime'] = datetime.datetime.utcnow()
    json_data = json.dumps(data)
    logging.info(json_data)
    ms.update(json_data)
    return json_data


def poll():
    while True:
        refresh()
        time.sleep(300)


def startServer():
    if "TRAVIS" not in os.environ:
        logging.info('starting server...')
        # Server settings
        # Choose port 8081, for port 80, which is normally used for
        # a http server, you need root access
        server_address = ('127.0.0.1', 8081)
        httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
        logging.info('running server...')
        httpd.serve_forever()
    else:
        time.sleep(300)


if __name__ == '__main__':
    if "TRAVIS" in os.environ:
        logLevel = logging.DEBUG
        logging.basicConfig(level=logLevel)

    ms = Message()
    pollThread = threading.Thread(target=poll)
    pollThread.daemon = True
    pollThread.start()

    mainThread = threading.Thread(target=startServer)
    mainThread.start()

    mainThread.join()
