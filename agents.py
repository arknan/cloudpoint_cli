#!/usr/bin/env python3

import sys
import api
import constants as co

def entry_point(args):

    endpoint = []
    if args.agents_command == 'show':
        endpoint.append(co.GETS_DICT[args.command])
        show(args, endpoint)
        output = getattr(api.Command(), co.METHOD_DICT['show'])('/'.join(endpoint))

    else:
        print("Invalid argument : '{}'".format(args.agents_command))
        sys.exit(-1)

    return output

def show(args, endpoint):

    if co.check_attr(args, 'agent_id'):
        endpoint.append(getattr(args, 'agent_id'))

    if (co.check_attr(args, 'agents_show_command')) and \
       (args.agents_show_command == "plugins"):
        if co.check_attr(args, 'agent_id'):
            endpoint.append("plugins/")
            if co.check_attr(args, 'plugin_name'):
                endpoint.append(args.plugin_name)

        else:
            print(co.EXIT_5)
            sys.exit(101)
        if co.check_attr(args, "configured_plugin_name"):
            endpoint.append(args.configured_plugin_name)
    elif (co.check_attr(args, 'agents_show_command')) and \
         (args.agents_show_command == "summary"):
        if co.check_attr(args, 'agent_id'):
            print("\nSummary cannot be provided for a specific agent\n")
            sys.exit(11)
        else:
            endpoint.append("summary")

def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format that makes parsing easier !
    print(data)
