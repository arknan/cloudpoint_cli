#!/usr/bin/env python3

import json
import sys
from texttable import Texttable
import api
import cloudpoint
import logs

LOG_C = logs.setup(__name__, 'c')


def entry_point(args):

    endpoint = ["classifications/tags"]
    LOG_C.info("Not Implemented")
    sys.exit(1)

def show(args, endpoint):
    pass


def pretty_print(args, output):
    print(output)
