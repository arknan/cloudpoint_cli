#!/usr/bin/env python3

import sys
import api
import cloudpoint
import logs

LOG_C = logs.setup(__name__, 'c')


def entry_point(args):

    endpoint = ['/plugins/']
    if args.plugins_command == 'show':
        show(args, endpoint)
        output = getattr(api.Command(), 'gets')('/'.join(endpoint))
    else:
        LOG_C.error("No arguments provided for 'plugins'")
        cloudpoint.run(["plugins", "-h"])
        sys.exit(1)

    return output


def show(args, endpoint):

    if api.check_attr(args, 'available_plugin_name'):
        endpoint.append(getattr(args, 'available_plugin_name'))

    if (api.check_attr(args, 'plugins_show_command')) and \
       (args.plugins_show_command == "description"):
        if api.check_attr(args, 'available_plugin_name'):
            endpoint.append("description")
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


def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format
    print(data)
