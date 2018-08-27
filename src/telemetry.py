#!/usr/bin/env python3

import json
import sys
from texttable import Texttable
import api
import cloudpoint
import logs

LOG_C = logs.setup(__name__, 'c')


def entry_point(args):

    endpoint = ['/telemetry/']

    if args.telemetry_command == 'disable':
        output = getattr(api.Command(), 'deletes')('/'.join(endpoint))

    elif args.telemetry_command == 'enable':
        data = None
        output = getattr(api.Command(), 'posts')('/'.join(endpoint), data)

    elif args.telemetry_command == 'status':
        output = getattr(api.Command(), 'gets')('/'.join(endpoint))

    else:
        LOG_C.error("No arguments provided for 'telemetry'")
        cloudpoint.run(["telemetry", "-h"])
        sys.exit(1)

    return output


def pretty_print(args, output):

    try:
        data = json.loads(output)
        table = Texttable()
        table.add_rows([(k, v) for k, v in sorted(data.items())], header=False)

        print(table.draw())

    except(KeyError, AttributeError):
        print(output)
