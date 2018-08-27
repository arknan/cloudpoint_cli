#!/usr/bin/env python3

import json
import texttable
import api


def entry_point(args):
    endpoint = ['/version']
    output = getattr(api.Command(), 'gets')('/'.join(endpoint))

    return output


def pretty_print(args, output):

    try:
        data = json.loads(output)
        table = texttable.Texttable()
        table.header([k for k, v in sorted(data.items())])
        table.add_row([v for k, v in sorted(data.items())])

        print(table.draw())

    except(KeyError, AttributeError, TypeError, NameError, texttable.ArraySizeError):
        print(output)
