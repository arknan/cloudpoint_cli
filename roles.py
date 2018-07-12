#!/usr/bin/env python3

import sys
import constants as co
import api

def entry_point(args):

    endpoint = []
    endpoint.append(co.GETS_DICT[args.command])
    if co.check_attr(args, 'reports_command'):
        globals()[args.reports_command](args, endpoint)
    else:
        print("Invalid argument : '{}'".format(args.reports_command))
        sys.exit(-1)

    output = getattr(api.Command(), co.METHOD_DICT[args.reports_command])('/'.join(endpoint))
    # Ideally this is where we would pass the output to a pretty printer function
    print(output)

