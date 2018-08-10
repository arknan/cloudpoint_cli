#!/usr/bin/env python3

import sys
import api
import cloudpoint
import logs

logger_c = logs.setup(__name__, 'c')


def entry_point(args):

    endpoint = ['/agents/']

    if args.agents_command == 'delete':
        delete(args, endpoint)
        output = getattr(api.Command(), 'deletes')('/'.join(endpoint))

    elif args.agents_command == 'show':
        show(args, endpoint)
        output = getattr(api.Command(), 'gets')('/'.join(endpoint))

    else:
        logger_c.error("No arguments provided for 'agents'")
        cloudpoint.run(["agents", "-h"])
        sys.exit(1)

    return output


def delete(args, endpoint):

    if api.check_attr(args, 'agents_delete_command'):
        endpoint.append(args.agent_id)

        if api.check_attr(args, 'agents_delete_agent_command'):
            endpoint.append('/' + args.agents_delete_agent_command)
            endpoint.append('/' + args.plugin_name)

            if api.check_attr(args, 'agents_delete_agent_plugins_command'):
                endpoint.append('/configs')
                endpoint.append('/' + args.config_id)
    else:
        logger_c.error("No arguments provided for 'delete'")
        cloudpoint.run(["agents", "delete", "-h"])
        sys.exit(1)


def show(args, endpoint):

    if api.check_attr(args, 'agent_id'):
        endpoint.append(args.agent_id)

        if api.check_attr(args, 'agents_show_command'):

            if args.agents_show_command == "plugins":
                endpoint.append("plugins/")

                if api.check_attr(args, "configured_plugin_name"):
                    endpoint.append(args.configured_plugin_name)

                    if api.check_attr(args, 'agents_show_plugins_command'):
                        endpoint.append('/configs/')

            elif args.agents_show_command == "summary":
                logger_c.error(
                    "Summary cannot be provided for a specific agent")
                sys.exit(1)
    else:
        if api.check_attr(args, 'agents_show_command'):
            if args.agents_show_command == 'summary':
                endpoint.append("summary")


def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format
    print(data)
