#!/usr/bin/env python3

import json
import sys
from texttable import Texttable
import api
import cloudpoint
import logs

LOG_C = logs.setup(__name__, 'c')


def entry_point(args):

    endpoint = ['/authorization/privilege/']
    if args.privileges_command == 'show':
        show(args, endpoint)
        output = getattr(
            api.Command(), 'gets')('/'.join(endpoint))

    else:
        LOG_C.error("No arguments provided for 'privileges'")
        cloudpoint.run(["privileges", "-h"])
        sys.exit(1)

    return output


def show(args, endpoint):
    if args.privilege_id:
        endpoint.append(args.privilege_id)


def pretty_print(args, output):
    print(output)
