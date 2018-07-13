#!/usr/bin/env python3

import sys
import api
import constants as co

def entry_point(args):

    endpoint = []
    if args.ldap_config_command == 'show':
        endpoint.append(co.GETS_DICT[args.command])
        show(args, endpoint)
        output = getattr(api.Command(), co.METHOD_DICT[args.ldap_config_command])('/'.join(endpoint))

    else:
        print("Invalid argument : '{}'".format(args.roles_command))
        sys.exit(-1)

    return output

def show(args, endpoint):
    # There is no work needed here, since our GETS_DICT provides
    # the whole endpoint ... retaining this for future ?
    pass

def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format that makes parsing easier !
    print(data)
