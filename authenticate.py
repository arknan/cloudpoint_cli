#!/usr/bin/env python3

import sys

import api
import constants as co

def entry_point(args):
    getattr(api.Command(), co.METHOD_DICT['authenticate'])()
    sys.exit(0)
