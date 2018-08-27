#!/usr/bin/env python3

import traceback
import json
import sys
import texttable
import api
import cloudpoint
import logs

LOG_C = logs.setup(__name__, 'c')
LOG_FC = logs.setup(__name__)


def entry_point(args):

    endpoint = ['/agents/']

    if args.agents_command == 'delete':
        delete(args, endpoint)
        output = getattr(api.Command(), 'deletes')('/'.join(endpoint))

    elif args.agents_command == 'show':
        print_args = show(args, endpoint)
        output = getattr(api.Command(), 'gets')('/'.join(endpoint))
        pretty_print(output, print_args)

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

    print_args = None
    if api.check_attr(args, 'agent_id'):
        endpoint.append(args.agent_id)
        print_args = "agent_id"

        if api.check_attr(args, 'agents_show_command'):
            if args.agents_show_command == "plugins":
                if api.check_attr(args, 'agent_id'):
                    endpoint.append("plugins/")
                    print_args = "plugins"

                else:
                    LOG_C.error("Plugins sub-command needs an agent_id")
                    sys.exit(1)

            else:
                LOG_C.error(
                    "Summary cannot be provided for a specific agent")
                sys.exit(1)

            if api.check_attr(args, "configured_plugin_name"):
                endpoint.append(args.configured_plugin_name)
                print_args = "plugin_id"

                if api.check_attr(args, 'agents_show_plugins_command'):
                    if api.check_attr(args, 'agent_id') and \
                       api.check_attr(args, "configured_plugin_name"):
                        endpoint.append('/configs/')
                        print_args = "configs"
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
        print_args = "base"
        if api.check_attr(args, 'agents_show_command'):
            if args.agents_show_command == 'summary':
                endpoint.append("summary")
                print_args = "summary"
            else:
                if api.check_attr(args, 'agents_show_plugins_command'):
                    LOG_C.error("Configs sub-command needs an agent_id \
and plugin_name")
                    sys.exit(1)
                else:
                    LOG_C.error("Plugins sub-command needs an agent_id")
                    sys.exit(1)

    return print_args


def pretty_print(output, print_args):

    try:
        data = json.loads(output)
        table = texttable.Texttable()
        if print_args  == "summary":
            table.header(["offhost", "onhost"])
            table.add_row([data["onHost"]["no"], data["onHost"]["yes"]])

        elif print_args == "base":
            required = ["agentid", "osName", "onHost", "status"]
            table.header(sorted(required))
            for i, _ in enumerate(data):
                table.add_row(
                    [v for k, v in sorted(data[i].items()) if k in required])

        elif print_args == "plugins":
            table.header(sorted(data[0].keys()))
            for i, _ in enumerate(data):
                table.add_row(
                    [v for k, v in sorted(data[i].items())])

        elif print_args == "plugin_id":
            table.add_rows([(k, v) for k, v in sorted(data.items())], header=False)
            
        elif print_args == "agent_id":
            ignored = ["hostname"]
            table.add_rows(
                [(k, v) for k, v in sorted(data.items()) if k not in ignored],
                header=False)

        elif print_args == "configs":
            ignored = ['configHash', 'configId']
            for i, _ in enumerate(data):
                table.add_rows(
                    [(k, v) for k, v in sorted(data[i].items())\
                    if k not in ignored], header=False)

        else:
            LOG_FC.critical("INTERNAL ERROR 1 IN '%s'", __file__)
            sys.exit(1)

        print(table.draw())

    except(KeyError, AttributeError, TypeError, NameError,
           texttable.ArraySizeError):
        print(output)
