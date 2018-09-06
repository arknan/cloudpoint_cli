#!/usr/bin/env python3

import json
import traceback
import texttable
import api
import logs
import utils

COLUMNS = utils.get_stty_cols()
LOG_F = logs.setup(__name__, 'f')


def entry_point(args):
    endpoint = ['/version']
    output = None
    print_args = None

    output = getattr(api.Command(), 'gets')('/'.join(endpoint))

    return output, print_args


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

        table.header([key for key, _ in sorted(data.items())])
        table.add_row([value for _, value in sorted(data.items())])

        if table.draw():
            print(table.draw())

    except(KeyError, AttributeError, TypeError, NameError,
           texttable.ArraySizeError, json.decoder.JSONDecodeError):
        LOG_F.critical(traceback.format_exc())
        print(output)
