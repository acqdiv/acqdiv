#!/usr/bin/python
# -*- coding: utf-8 -*-
# Created by Cazim Hysi @ UZH
# cazim dot hysi at gmail dot com

import os
import sys
import collections

class CdcParser():

    def __init__(self, path):

        self.metadata = {}
        # loop through each line of the .cdc file and gather its contents
        with open(path, "r") as file:
            for line in file:
                # process each line; if no ":" skip the line
                line = line.strip()
                line = line.replace("\t", "")
                if not line.__contains__(":"):
                    continue
                tokens = line.partition(":")
                property = tokens[0]
                data = tokens[2].strip()
                self.metadata[property] = data



