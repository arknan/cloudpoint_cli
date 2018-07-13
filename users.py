#!/usr/bin/env python3

import sys
import api
import constants as co

def entry_point(args):

    endpoint = []
    endpoint.append(co.GETS_DICT[args.command])
    if co.check_attr(args, 'users_command'):
        globals()[args.users_command](args, endpoint)
    else:
        print("Invalid argument : '{}'".format(args.users_command))
        sys.exit(-1)

    output = getattr(api.Command(), co.METHOD_DICT[args.users_command])('/'.join(endpoint))
    return output

def show(args, endpoint):
    if co.check_attr(args, 'user_id'):
        endpoint.append(args.user_id)

    return endpoint

def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format that makes parsing easier !
    print(data)
