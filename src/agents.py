#!/usr/bin/env python3

import json
import sys
from texttable import Texttable
import api
import cloudpoint
import logs

LOG_C = logs.setup(__name__, 'c')


def entry_point(args):

    endpoint = ['/agents/']

    if args.agents_command == 'delete':
        delete(args, endpoint)
        output = getattr(api.Command(), 'deletes')('/'.join(endpoint))

    elif args.agents_command == 'show':
        show(args, endpoint)
        output = getattr(api.Command(), 'gets')('/'.join(endpoint))

    else:
        LOG_C.error("No arguments provided for 'agents'")
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
        LOG_C.error("No arguments provided for 'delete'")
        cloudpoint.run(["agents", "delete", "-h"])
        sys.exit(1)


def show(args, endpoint):

    if api.check_attr(args, 'agent_id'):
        endpoint.append(args.agent_id)

        if api.check_attr(args, 'agents_show_command'):

            if args.agents_show_command == "plugins":
                if api.check_attr(args, 'agent_id'):
                    endpoint.append("plugins/")
                else:
                    LOG_C.error("Plugins sub-command needs an agent_id")
                    sys.exit(1)

            else:
                LOG_C.error(
                    "Summary cannot be provided for a specific agent")
                sys.exit(1)

            if api.check_attr(args, "configured_plugin_name"):
                endpoint.append(args.configured_plugin_name)

                if api.check_attr(args, 'agents_show_plugins_command'):
                    if api.check_attr(args, 'agent_id') and \
                       api.check_attr(args, "configured_plugin_name"):
                        endpoint.append('/configs/')
                    else:
                        LOG_C.error("Configs sub-command needs an \
agent_id and plugin_name")
                        sys.exit(1)

            else:
                if api.check_attr(args, 'agents_show_plugins_command'):
                    LOG_C.error("Configs sub-command needs an agent_id \
and plugin_name")
                    sys.exit(1)

    else:
        if api.check_attr(args, 'agents_show_command'):
            if args.agents_show_command == 'summary':
                endpoint.append("summary")
            else:
                if api.check_attr(args, 'agents_show_plugins_command'):
                    LOG_C.error("Configs sub-command needs an agent_id \
and plugin_name")
                    sys.exit(1)
                else:
                    LOG_C.error("Plugins sub-command needs an agent_id")
                    sys.exit(1)


def pretty_print(output, args):

    data = json.loads(output)
    print_fields = ["agentid", "osName", "onHost", "status"]
    table = Texttable()
    table.header(sorted(print_fields))

    def cleanse(data):
        for k in list(data.keys()):
            if k not in print_fields:
                del data[k]
    
    if api.check_attr(args, 'agent_id'):
        table.add_row(list(v for k, v in sorted(data.items()) if k in print_fields))
        cleanse(data)
    else:
        for i, _ in enumerate(data):
            cleanse(data[i])
            table.add_row(list(v for k, v in sorted(data[i].items()) if k in print_fields))

    print(table.draw())
