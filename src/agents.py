#!/usr/bin/env python3

import datetime
import json
import sys
import traceback
import texttable
import api
import cloudpoint
import logs
import utils

COLUMNS = utils.get_stty_cols()
LOG_C = logs.setup(__name__, 'c')
LOG_F = logs.setup(__name__, 'f')
LOG_FC = logs.setup(__name__)


def entry_point(args):

    endpoint = ['/agents/']

    if args.agents_command == 'delete':
        delete(args, endpoint)
        output = getattr(api.Command(), 'deletes')('/'.join(endpoint))
        pretty_print(output, "delete")

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

    if utils.check_attr(args, 'agents_delete_command'):
        endpoint.append(args.agent_id)

        if utils.check_attr(args, 'agents_delete_agent_command'):
            endpoint.append('/' + args.agents_delete_agent_command)
            endpoint.append('/' + args.plugin_name)

            if utils.check_attr(args, 'agents_delete_agent_plugins_command'):
                endpoint.append('/configs')
                endpoint.append('/' + args.config_id)
    else:
        LOG_C.error("No arguments provided for 'delete'")
        cloudpoint.run(["agents", "delete", "-h"])
        sys.exit(1)


def show(args, endpoint):

    print_args = None
    if utils.check_attr(args, 'agent_id'):
        endpoint.append(args.agent_id)
        print_args = "agent_id"

        if utils.check_attr(args, 'agents_show_command'):
            if args.agents_show_command == "plugins":
                if utils.check_attr(args, 'agent_id'):
                    endpoint.append("plugins/")
                    print_args = "plugins"

                else:
                    LOG_C.error("Plugins sub-command needs an agent_id")
                    sys.exit(1)

            else:
                LOG_C.error(
                    "Summary cannot be provided for a specific agent")
                sys.exit(1)

            if utils.check_attr(args, "configured_plugin_name"):
                endpoint.append(args.configured_plugin_name)
                print_args = "plugin_id"

                if utils.check_attr(args, 'agents_show_plugins_command'):
                    if utils.check_attr(args, 'agent_id') and \
                       utils.check_attr(args, "configured_plugin_name"):
                        endpoint.append('/configs/')
                        print_args = "configs"
                    else:
                        LOG_C.error("Configs sub-command needs an \
agent_id and plugin_name")
                        sys.exit(1)

            else:
                if utils.check_attr(args, 'agents_show_plugins_command'):
                    LOG_C.error("Configs sub-command needs an agent_id \
and plugin_name")
                    sys.exit(1)

    else:
        print_args = "show"
        if utils.check_attr(args, 'agents_show_command'):
            if args.agents_show_command == 'summary':
                endpoint.append("summary")
                print_args = "summary"
            else:
                if utils.check_attr(args, 'agents_show_plugins_command'):
                    LOG_C.error("Configs sub-command needs an agent_id \
and plugin_name")
                    sys.exit(1)
                else:
                    LOG_C.error("Plugins sub-command needs an agent_id")
                    sys.exit(1)

    return print_args


def pretty_print(output, print_args):

    try:
        table = texttable.Texttable(max_width=COLUMNS)
        data = json.loads(output)
        pformat = utils.print_format()

        if pformat == 'json':
            print_args = 'json'
        else:
            table.set_deco(pformat)

        if print_args == "agent_id":
            table.header(("Attribute", "Value"))
            ignored = ["hostname"]
            klist = []
            vlist = []
            for k, v in sorted(data.items()):
                if k not in ignored:
                    klist.append(k.upper())
                    if k == "onHost":
                        vlist.append(str(bool(v)))
                    elif k == "osName":
                        vlist.append(v.capitalize())
                    elif k == "lastMessage":
                        vlist.append(datetime.datetime.fromtimestamp(v))
                    else:
                        vlist.append(v)

                if klist and vlist:
                    table.add_row([klist.pop(), vlist.pop()])

        elif print_args == "configs":
            table.header(("Attribute", "Value"))
            ignored = ['configHash', 'configId']
            for i, _ in enumerate(data):
                table.add_rows(
                    [(k.upper(), v) for k, v in sorted(data[i].items())
                    if k not in ignored], header=False)

        elif print_args == 'json':
            print(output)

        elif print_args == "show":
            required = ["agentid", "osName", "onHost", "status"]
            for i, _ in enumerate(data):
                klist = []
                vlist = []
                for k, v in sorted(data[i].items()):
                    if k in required:
                        klist.append(k.upper())
                        if k == "onHost":
                            vlist.append(str(bool(v)))
                        elif k == "osName":
                            vlist.append(v.capitalize())
                        else:
                            vlist.append(v)

                if klist and vlist:
                    table.add_rows((klist, vlist))

        elif print_args  == "summary":
            table.header(["OFFHOST", "ONHOST"])
            table.add_row([data["onHost"]["no"], data["onHost"]["yes"]])

        elif print_args == "plugins":
            table.header([k.upper() for k in sorted(data[0].keys())])
            table.set_cols_dtype(['t', 't', 't'])
            for i, _ in enumerate(data):
                table.add_row(
                    [v for k, v in sorted(data[i].items())])

        elif print_args == "plugin_id":
            table.header(("Attribute", "Value"))
            table.set_cols_dtype(['t', 't'])
            table.add_rows([(k.upper(), v) for k, v in sorted(data.items())], header=False)
            
        else:
            table.header(("Attribute", "Value"))
            table.add_rows(
                [(k.upper(), v) for k, v in sorted(data[i].items())], header=False)

        if table.draw():
            print(table.draw())

    except Exception:
        LOG_F.critical(traceback.format_exc())
        print(output)
