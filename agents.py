#!/usr/bin/env python3

import sys
import api
import constants as co
import cldpt


def entry_point(args):

    endpoint = ['/agents/']

    if args.agents_command == 'delete':
        delete(args, endpoint)
        output = getattr(api.Command(), 'deletes')('/'.join(endpoint))

    elif args.agents_command == 'show':
        show(args, endpoint)
        output = getattr(api.Command(), 'gets')('/'.join(endpoint))

    else:
        print("No arguments provided for 'agents'\n")
        cldpt.run(["agents", "-h"])
        sys.exit(-1)

    return output


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


def show(args, endpoint):

    if co.check_attr(args, 'agent_id'):
        endpoint.append(args.agent_id)

        if co.check_attr(args, 'agents_show_command'):
            if args.agents_show_command == "plugins":
                endpoint.append("plugins/")
                if co.check_attr(args, "configured_plugin_name"):
                    endpoint.append(args.configured_plugin_name)
                    if co.check_attr(args, 'agents_show_plugins_command'):
                        endpoint.append('/configs/')

            elif args.agents_show_command == "summary":
                print("\nSummary cannot be provided for a specific agent\n")
                sys.exit(11)
    else:
        if co.check_attr(args, 'agents_show_command'):
            if args.agents_show_command == 'summary':
                endpoint.append("summary")


def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format
    print(data)
