#!/usr/bin/env python3

import sys
import api
import constants as co

def entry_point(args):

    endpoint = []
    endpoint.append(co.GETS_DICT[args.command])
    if co.check_attr(args, 'privileges_command'):
        endpoint = globals()[args.privileges_command](args, endpoint)
    else:
        print("Invalid Command : {}".format(args.privileges_command))
        sys.exit(-1)
    
    output = getattr(api.Command(), co.METHOD_DICT[args.privileges_command])('/'.join(endpoint))
    return output

def show(args, endpoint):
    if co.check_attr(args, 'privilege_id'):
        endpoint.append(args.privilege_id)

    return endpoint

def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format that makes parsing easier !
    print(data)
