#!/usr/bin/env python3

import sys
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


def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format
    print(data)
