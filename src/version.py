#!/usr/bin/env python3

import json
from texttable import Texttable
import api


def entry_point(args):
    endpoint = ['/version']
    output = getattr(api.Command(), 'gets')('/'.join(endpoint))

    return output


def pretty_print(args, output):

    data = json.loads(output)
    table = Texttable()
    table.header([k for k, v in sorted(data.items())])
    for i, _ in enumerate(data):
        table.add_row(list(v for k, v in sorted(data.items())))

    print(table.draw())

