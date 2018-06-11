#!/usr/bin/env python3

import sys
import constants
import json
from pprint import pprint


def check_attr(args, attr):

    try:
        if hasattr(args, attr):
            if getattr(args, attr):
                return True
    except NameError:
        return False
    else:
        return False


def common_paths(endpoint, args):

    if args.show_command == "policies":
        detail = "policy_id"
    else:
        detail = (args.show_command)[:-1] + '_id'
    if check_attr(args, detail):
        endpoint.append(getattr(args, detail))

    return endpoint


def roles(args):

    data = None
    if check_attr(args, 'file_name'):
        with open(getattr(args, 'file_name'), 'r') as f:
            data = json.load(f)

    pprint(data)
    return data
