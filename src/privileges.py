#!/usr/bin/env python3

import json
import sys
import traceback
import texttable
import api
import cloudpoint
import logs
import utils

COLUMNS = utils.get_stty_cols()
LOG_C = logs.setup(__name__, 'c')
LOG_F = logs.setup(__name__, 'f')


def entry_point(args):

    endpoint = ['/authorization/privilege/']
    output = None
    print_args = None

    if args.privileges_command == 'show':
        print_args = show(args, endpoint)
        output = getattr(
            api.Command(), 'gets')('/'.join(endpoint))

    else:
        LOG_C.error("No arguments provided for 'privileges'")
        cloudpoint.run(["privileges", "-h"])
        sys.exit(1)

    return output, print_args


def show(args, endpoint):

    print_args = None
    if args.privilege_id:
        endpoint.append(args.privilege_id)
        print_args = "privilege_id"

    else:
        print_args = "show"

    return print_args


def pretty_print(output, print_args):

    try:
        data = json.loads(output)
        table = texttable.Texttable(max_width=COLUMNS)
        pformat = utils.print_format()

        if pformat == 'json':
            print(output)
            sys.exit(0)
        else:
            table.set_deco(pformat)

        if print_args == "privilege_id":
            ignored = ["links"]
            table.header(["Attribute", "Value"])
            table.set_cols_dtype(['t', 't'])
            table.add_rows(
                [(k, v) for k, v in sorted(data.items()) if k not in ignored],
                header=False)
        else:
            required = ["name", "id"]
            table.header([i.capitalize() for i in required])

            for i, _ in enumerate(data):
                table.add_row(
                    [v for k, v in reversed(sorted(data[i].items())) if k in required])

        if table.draw():
            print(table.draw())

    except(KeyError, AttributeError, TypeError, NameError,
           texttable.ArraySizeError, json.decoder.JSONDecodeError):
        LOG_F.critical(traceback.format_exc())
        print(output)
