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
    return output

def show(args, endpoint):
    # There is no work needed here, since our GETS_DICT provides
    # the whole endpoint ... retaining this for future ?
    return endpoint

def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format that makes parsing easier !
    print(data)
