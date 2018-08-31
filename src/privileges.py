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

    endpoint = ['/authorization/privilege/']
    if args.privileges_command == 'show':
        print_args = show(args, endpoint)
        output = getattr(
            api.Command(), 'gets')('/'.join(endpoint))
        pretty_print(output, print_args)

    else:
        LOG_C.error("No arguments provided for 'privileges'")
        cloudpoint.run(["privileges", "-h"])
        sys.exit(1)

    return output


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
        table.set_deco(texttable.Texttable.HEADER)

        if print_args == "privilege_id":
            ignored = ["links"]
            table.add_rows(
                [(k, v) for k, v in sorted(data.items()) if k not in ignored],
                header=False)
        else:
            required = ["id", "name"]
            table.header(sorted(required))

            for i, _ in enumerate(data):
                table.add_row(
                    [v for k, v in sorted(data[i].items()) if k in required])

        if table.draw():
            print(table.draw())

    except(KeyError, AttributeError, TypeError, NameError, texttable.ArraySizeError, json.decoder.JSONDecodeError):
        print(output)
