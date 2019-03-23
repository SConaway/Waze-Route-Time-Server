#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

import WazeRouteCalculator


class Route:
    def __init__(self, f, t, re, logLevel):
        self.from_address = f
        self.to_address = t
        self.region = re
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
            import time
            time.sleep(10)
            del time
            results = self.get_info()
        # TODO: convert to miles if unit is mi
        time = round(results[0], 2)
        dist = round(results[1], 2)
        color = "default"
        return time, dist, self.units, color
