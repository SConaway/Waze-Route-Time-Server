#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import WazeRouteCalculator
import yaml
import os.path
import time
import logging
import json

logLevel = logging.DEBUG
logging.basicConfig(level=logLevel)


yamlFilePath = "example-config.yaml"
if os.path.isfile("config.yml"):
    yamlFilePath = "config.yml"
if os.path.isfile("config.yaml"):
    yamlFilePath = "config.yaml"
logging.info("Config File: %s", yamlFilePath)

message = '{"message": "Check back later. Server is still starting."}'


def getTime(from_address, to_address, region):
    route = WazeRouteCalculator.WazeRouteCalculator(
        from_address, to_address, region, log_lvl=logLevel)
    try:
        results = route.calc_route_info()
    except WazeRouteCalculator.WRCError as err:
        logging.info("Sleeping for 10 seconds due to error: " + str(err))
        time.sleep(10)
        results = getTime(from_address, to_address, region)
    if region == "US" or region == "NA":
        units = "mi"
    else:
        units = "km"
    return(round(results[0], 2), round(results[1], 2), units)


def getTimes():
    logging.info("Getting Times")
    print("hi")
    with open(yamlFilePath, 'r') as f:
        config = yaml.load(f)
    logging.info(config)
    data = {}
    # data['key'] = 'value'
    json_data = json.dumps(data)
    i = 0
    for route in config:
        i = i + 1
        logging.info(config[route])
        routeTime, routeDist, routeUnits = getTime(
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
        data[i] = str
        time.sleep(1)
    json_data = json.dumps(data)
    logging.info(json_data)
    message = json_data
    return json_data


def refresh():
    while True:
        getTimes()
        time.sleep(60)


class HTTPServer_RequestHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Send message back to client as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return


def startServer():
    logging.info('starting server...')

    # Server settings
    # Choose port 8081, for port 80, which is normally used for
    # a http server, you need root access
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
    logging.info('running server...')
    httpd.serve_forever()


if __name__ == '__main__':
    # formatMessage(getTimes)
    # threading.Timer(5.0, formatMessage(getTimes)).start()
    # threading.Timer(5.0, getTimes).start()
    thread1 = threading.Thread(target=refresh)
    thread1.start()
    # thread1.join()

    if "TRAVIS" not in os.environ:
        thread2 = threading.Thread(target=startServer)
        thread2.start()
        # thread2.join()
    else:
        time.sleep(60)
