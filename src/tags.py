#!/usr/bin/env python3

import json
import sys
import texttable
import api
import cloudpoint
import logs

COLUMNS = api.get_stty_cols()
LOG_C = logs.setup(__name__, 'c')


def entry_point(args):

    endpoint = ["classifications/tags"]
    LOG_C.info("Not Implemented")
    sys.exit(1)


def show(args, endpoint):
    pass


def pretty_print(output, print_args):
    try:
        print(output)
    except(KeyError, AttributeError, TypeError, NameError, texttable.ArraySizeError, json.decoder.JSONDecodeError):
        print(output)
