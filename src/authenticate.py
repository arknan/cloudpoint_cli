#!/usr/bin/env python3

import sys
import api


def entry_point(args):
    getattr(api.Command(), 'authenticates')()
    sys.exit(1)
