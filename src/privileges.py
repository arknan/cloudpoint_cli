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
    
    data = json.loads(output)
    table = Texttable()

    if args.privilege_id:
        ignored = ["links"]
        table.add_rows(
            [(k, v) for k, v in sorted(data.items()) if not k in ignored],
            header=False)
    else:
        required = ["id", "name"]
        table.header(sorted(required))

        for i, _ in enumerate(data):
            table.add_row([v for k, v in sorted(data[i].items()) if k in required])

    if table.draw():
        print(table.draw())
