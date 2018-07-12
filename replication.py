#!/usr/bin/env python3

import sys
import api
import constants as co

def entry_point(args):

    endpoint = []
    endpoint.append(co.GETS_DICT[args.command])
    if co.check_attr(args, 'replication_command'):
        globals()[args.replication_command](args, endpoint)
    else:
        print("Invalid argument : '{}'".format(args.replication_command))
        sys.exit(-1)

    output = getattr(api.Command(), co.METHOD_DICT[args.replication_command])('/'.join(endpoint))
    # Ideally this is where we would pass the output to a pretty printer function
    print(output)


def show(args, endpoint):

    if co.check_attr(args, 'policy_name'):
        endpoint.append(getattr(args, 'policy_name'))

    if co.check_attr(args, 'replication_show_command'):
        if co.check_attr(args, 'policy_name'):
            endpoint.append('/rules/')
        else:
            print("Mention a policy name to get replication rules\n")
            sys.exit(-1)

    return endpoint
