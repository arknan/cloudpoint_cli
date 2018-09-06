#!/usr/bin/env python3

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


def entry_point(args):

    endpoint = ['/plugins/']
    if args.plugins_command == 'show':
        print_args = show(args, endpoint)
        output = getattr(api.Command(), 'gets')('/'.join(endpoint))

    else:
        LOG_C.error("No arguments provided for 'plugins'")
        cloudpoint.run(["plugins", "-h"])
        sys.exit(1)

    return output, print_args


def show(args, endpoint):

    print_args = None
    if utils.check_attr(args, 'available_plugin_name'):
        plugin_cmd = json.loads(cloudpoint.run(["plugins", "show"]))
        plugin_list = []
        for i, _ in enumerate(plugin_cmd):
            for key, value in sorted(plugin_cmd[i].items()):
                if key == "name":
                    plugin_list.append(value)
        if args.available_plugin_name in plugin_list:
            endpoint.append(args.available_plugin_name)
            print_args = 'available_plugin_name'

        if utils.check_attr(args, 'plugins_show_command'):
            if args.plugins_show_command == "description":
                endpoint.append("description")
                print_args = "description"

            elif args.plugins_show_command == "summary":
                LOG_C.error("Summary cannot be provided for a specific plugin")
                sys.exit(1)

    else:
        if utils.check_attr(args, 'plugins_show_command'):
            if args.plugins_show_command == "description":
                LOG_C.error("'description' requires -i flag for 'PLUGIN_NAME'")
                sys.exit(1)
            elif args.plugins_show_command == "summary":
                endpoint.append("summary")
                print_args = "summary"
        else:
            print_args = "show"

    return print_args


def pretty_print(output, print_args, pformat=utils.print_format()):

    try:
        table = texttable.Texttable(max_width=COLUMNS)
        data = json.loads(output)

        if pformat == 'json':
            print(output)
            sys.exit(0)
        else:
            table.set_deco(pformat)

        if print_args == 'available_plugin_name':
            table.set_cols_dtype(['t', 't'])
            table.add_rows(
                [(key, value) for key, value in sorted(data.items())
                 if key != "configTemplate"], header=False)

            for i, _ in enumerate(data["configTemplate"]):
                table.add_rows([("", "")], header=False)
                table.add_rows(
                    [(key, value) for key, value in sorted(
                        data["configTemplate"][i].items())], header=False)

        elif print_args == 'description':
            print(output)
            sys.exit(0)

        elif print_args == "show":
            required = ["displayName", "name", "onHost", "version"]
            table.header(sorted(required))
            table.set_cols_dtype(['t', 't', 't', 't'])
            for i, _ in enumerate(data):
                table.add_row(
                    [value for key, value in sorted(data[i].items())
                     if key in required])

        elif print_args == "summary":
            table.header(["", "onHost", "offHost"])
            table.add_row(["configured", data["onHost"]["yes"]["configured"],
                           data["onHost"]["no"]["configured"]])
            table.add_row(["supported", data["onHost"]["yes"]["supported"],
                           data["onHost"]["no"]["supported"]])

        else:
            table.header(("Attribute", "Value"))
            table.add_rows(
                [(key, value) for key, value in sorted(data.items())],
                header=False)

        if table.draw():
            print(table.draw())

    except(KeyError, AttributeError, TypeError, NameError,
           texttable.ArraySizeError, json.decoder.JSONDecodeError):
        LOG_F.critical(traceback.format_exc())
        print(output)
