#!/usr/bin/env python3

import sys
import api
import constants as co

def entry_point(args):

    endpoint = []
    endpoint.append(co.GETS_DICT[args.command])
    if co.check_attr(args, 'email_config_command'):
        globals()[args.email_config_command](args, endpoint)
    else:
        print("Invalid argument : '{}'".format(args.email_config_command))
        sys.exit(-1)

    output = getattr(api.Command(), co.METHOD_DICT[args.email_config_command])('/'.join(endpoint))
    # Ideally this is where we would pass the output to a pretty printer function
    print(output)


def show(args, endpoint):
    # There is no work needed here, since our GETS_DICT provides
    # the whole endpoint ... retaining this for future ?
    return endpoint
