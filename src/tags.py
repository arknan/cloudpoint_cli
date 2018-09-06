#!/usr/bin/env python3

import json
import sys
import traceback
import texttable
# import api
# import cloudpoint
import logs
import utils

COLUMNS = utils.get_stty_cols()
LOG_C = logs.setup(__name__, 'c')
LOG_F = logs.setup(__name__, 'f')


def entry_point(args):

    endpoint = ["classifications/tags"]
    show(args, endpoint)
    LOG_C.info("Not Implemented")
    sys.exit(1)


def show(args, endpoint):
    pass


def pretty_print(output, print_args):
    try:
        print(output)
    except(KeyError, AttributeError, TypeError, NameError,
           texttable.ArraySizeError, json.decoder.JSONDecodeError):
        LOG_F.critical(traceback.format_exc())
        print(output)
