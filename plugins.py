#!/usr/bin/env python3

import sys
import api
import constants as co

def entry_point(args):

    endpoint = []
    endpoint.append(co.GETS_DICT[args.command])
    if co.check_attr(args, 'plugins_command'):
        try:
            globals()[args.plugins_command](args, endpoint)
        except KeyError:
            print("Internal Error: Function '{}' doesn't exist".format(args.plugins_command))
            sys.exit(-1)
    else:
        print("No argument provided for command '{}'".format(args.command))
        sys.exit(-1)

    print(endpoint)
    output = getattr(api.Command(), co.METHOD_DICT[args.plugins_command])('/'.join(endpoint))
    return output

def show(args, endpoint):

    if co.check_attr(args, 'available_plugin_name'):
        endpoint.append(getattr(args, 'available_plugin_name'))

    if (co.check_attr(args, 'plugins_show_command')) and \
       (args.plugins_show_command == "description"):
        if co.check_attr(args, 'available_plugin_name'):
            endpoint.append("description")
        else:
            print(co.EXIT_6)
            sys.exit(102)
    elif (co.check_attr(args, 'plugins_show_command')) and \
         (args.plugins_show_command == "summary"):
        if co.check_attr(args, 'available_plugin_name'):
            print("\nSummary cannot be provided for a specific plugin\n")
            sys.exit(12)
        else:
            endpoint.append("summary")

    return endpoint


def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format that makes parsing easier !
    print(data)
