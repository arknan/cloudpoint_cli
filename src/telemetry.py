#!/usr/bin/env python3

import json
import sys
import texttable
import api
import cloudpoint
import logs
import utils

COLUMNS = utils.get_stty_cols()
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
        pretty_print(output, None)

    else:
        LOG_C.error("No arguments provided for 'telemetry'")
        cloudpoint.run(["telemetry", "-h"])
        sys.exit(1)

    return output


def pretty_print(output, print_args):

    try:
        data = json.loads(output)
        table = texttable.Texttable(max_width=COLUMNS)
        table.set_deco(texttable.Texttable.HEADER)
        table.add_rows([(k, v) for k, v in sorted(data.items())], header=False)

        print(table.draw())

    except(KeyError, AttributeError, TypeError, NameError, texttable.ArraySizeError, json.decoder.JSONDecodeError):
        print(output)
