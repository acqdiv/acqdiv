#!/usr/bin/python
# -*- coding: utf-8 -*-
# Created by Cazim Hysi @ UZH
# cazim.hysi@gmail.com

import os
import sys
import collections

class CdcParser():

    def __init__(self, path):
        self.metadata = {}
        for root, subs, files in os.walk(path):
            for file in files:
                if file.__contains__("metadata"):
                    filepath = os.path.join(root, file)

                    # loop through each line of the .cdc file and gather its contents
                    with open(filepath, "r") as file:
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



