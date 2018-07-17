#!/usr/bin/env python3

import sys
import api
import constants as co
import cldpt

def entry_point(args):

    endpoint = []
    if args.agents_command == 'show':
        endpoint.append(co.GETS_DICT[args.command])
        show(args, endpoint)
        output = getattr(api.Command(), co.METHOD_DICT['show'])(
            '/'.join(endpoint))

    elif args.agents_command == 'delete':
        endpoint.append(co.GETS_DICT[args.command])
        delete(args, endpoint)
        print(endpoint)
        output = getattr(api.Command(), 'deletes')('/'.join(endpoint))

    else:
        print("No arguments provided for 'agents'\n")
        cldpt.run(["agents", "-h"])
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
            if co.check_attr(args, 'agents_show_plugins_command'):
                endpoint.append('/configs/')
    elif (co.check_attr(args, 'agents_show_command')) and \
         (args.agents_show_command == "summary"):
        if co.check_attr(args, 'agent_id'):
            print("\nSummary cannot be provided for a specific agent\n")
            sys.exit(11)
        else:
            endpoint.append("summary")


def delete(args, endpoint):

    if co.check_attr(args, 'agents_delete_command'):
            endpoint.append(args.agent_id) 
            if co.check_attr(args, 'agents_delete_agent_command'):
                endpoint.append('/' + args.agents_delete_agent_command)
                endpoint.append('/' + args.plugin_name)
            if co.check_attr(args, 'agents_delete_agent_plugins_command'):
                 endpoint.append('/configs')
                 endpoint.append('/' + args.config_id)
    else:
        cldpt.run(["agents", "delete", "-h"])
def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format
    print(data)
