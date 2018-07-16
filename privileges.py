#!/usr/bin/env python3

import sys
import api
import cldpt
import constants as co


def entry_point(args):

    endpoint = []
    if args.privileges_command == 'show':
        endpoint.append(co.GETS_DICT[args.command])
        show(args, endpoint)
        output = getattr(
            api.Command(), co.METHOD_DICT[args.privileges_command])(
                '/'.join(endpoint))

    else:
        print("No arguments provided for 'privileges'\n")
        cldpt.run(["privileges", "-h"])
        sys.exit(-1)

    return output


def show(args, endpoint):
    if args.privilege_id:
        endpoint.append(args.privilege_id)


def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format
    print(data)
