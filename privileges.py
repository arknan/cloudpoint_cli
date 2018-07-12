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
    print(output)

def show(args, endpoint):
    if co.check_attr(args, 'privilege_id'):
        endpoint.append(args.privilege_id)

    return endpoint
