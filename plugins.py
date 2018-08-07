#!/usr/bin/env python3

import sys
import api
import cloudpoint
import constants as co


def entry_point(args):

    endpoint = []
    if args.plugins_command == 'show':
        endpoint.append(co.GETS_DICT[args.command])
        show(args, endpoint)
        output = getattr(
            api.Command(), co.METHOD_DICT[args.plugins_command])(
                '/'.join(endpoint))
    else:
        print("No arguments provided for 'plugins'\n")
        cloudpoint.run(["plugins", "-h"])
        sys.exit(-1)

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


def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format
    print(data)
