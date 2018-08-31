#!/usr/bin/env python3

import json
import sys
import texttable
import api
import cloudpoint
import logs

LOG_C = logs.setup(__name__, 'c')


def entry_point(args):

    endpoint = ['/plugins/']
    if args.plugins_command == 'show':
        print_args = show(args, endpoint)
        output = getattr(api.Command(), 'gets')('/'.join(endpoint))
        pretty_print(output, print_args)

    else:
        LOG_C.error("No arguments provided for 'plugins'")
        cloudpoint.run(["plugins", "-h"])
        sys.exit(1)

    return output


def show(args, endpoint):

    print_args = None
    if api.check_attr(args, 'available_plugin_name'):
        plugin_cmd = json.loads(cloudpoint.run(["plugins", "show"]))
        plugin_list = []
        for i, _ in enumerate(plugin_cmd):
            for k, v in sorted(plugin_cmd[i].items()):
                if k == "name":
                    plugin_list.append(v)
        if args.available_plugin_name in plugin_list:
            endpoint.append(args.available_plugin_name)
            print_args = 'available_plugin_name'

        else:
            LOG_C.error("Please provide a valid plugin name (ex: mongo)")
            sys.exit(1)

    if (api.check_attr(args, 'plugins_show_command')) and \
       (args.plugins_show_command == "description"):
        if api.check_attr(args, 'available_plugin_name'):
            endpoint.append("description")
            print_args = "description"

        else:
            LOG_C.error("'description' requires -i flag for 'PLUGIN_NAME'")
            sys.exit(1)

    elif (api.check_attr(args, 'plugins_show_command')) and \
         (args.plugins_show_command == "summary"):
        if api.check_attr(args, 'available_plugin_name'):
            LOG_C.error("Summary cannot be provided for a specific plugin")
            sys.exit(1)
        else:
            endpoint.append("summary")
            print_args = "summary"

    else:
        print_args = "show"

    return print_args


def pretty_print(output, print_args):

    try:
        if pretty_print == "description":
            print(output)
            sys.exit(0)

        data = json.loads(output)
        table = texttable.Texttable()

        if print_args == 'available_plugin_name':
            table.add_rows(
                [(k, v) for k, v in sorted(data.items()) if k != "configTemplate"],
                header=False)

            for i, _ in enumerate(data["configTemplate"]):
                table.add_rows([("", "")], header=False)
                table.add_rows(
                    [(k, v) for k, v in sorted(data["configTemplate"][i].items())],
                    header=False)

        elif print_args == "summary":
            table.header(["", "onHost", "offHost"])
            table.add_row(["configured", data["onHost"]["yes"]["configured"],
                           data["onHost"]["no"]["configured"]])
            table.add_row(["supported", data["onHost"]["yes"]["supported"],
                           data["onHost"]["no"]["supported"]])

        else:
            required = ["displayName", "name", "onHost"]
            table.header(sorted(required))
            for i, _ in enumerate(data):
                table.add_row(
                    [v for k, v in sorted(data[i].items()) if k in required])

        print(table.draw())
    except(KeyError, AttributeError, TypeError, NameError, texttable.ArraySizeError, json.decoder.JSONDecodeError):
        print(output)
