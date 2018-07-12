#!/usr/bin/env python3

import sys
import api
import constants as co

def entry_point(args):

    endpoint = []
    endpoint.append(co.GETS_DICT[args.command])
    if co.check_attr(args, 'policies_command'):
        globals()[args.policies_command](args, endpoint)
    else:
        print("Invalid argument : '{}'".format(args.policies_command))
        sys.exit(-1)

    output = getattr(api.Command(), co.METHOD_DICT[args.policies_command])('/'.join(endpoint))
    # Ideally this is where we would pass the output to a pretty printer function
    print(output)

def show(args, endpoint):
    
    if co.check_attr(args, 'policy_id'):
        endpoint.append(args.policy_id)

    return endpoint
