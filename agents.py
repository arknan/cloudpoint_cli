#!/usr/bin/env python3

import sys
import api
import constants as co

def entry_point(args):

    endpoint = []
    endpoint.append(co.GETS_DICT[args.command])
    if co.check_attr(args, 'agents_command'):
        globals()[args.agents_command](args, endpoint)
    else:
        print("Invalid argument : '{}'".format(args.agents_command))
        sys.exit(-1)

    output = getattr(api.Command(), co.METHOD_DICT[args.agents_command])('/'.join(endpoint))
    # Ideally this is where we would pass the output to a pretty printer function
    print(output)    

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

    return endpoint
