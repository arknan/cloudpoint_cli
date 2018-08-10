#!/usr/bin/env python3

import sys
import api
import cloudpoint
import constants as co
import logs

logger_c = logs.setup(__name__, 'c')


def entry_point(args):

    endpoint = ['/plugins/']
    if args.plugins_command == 'show':
        show(args, endpoint)
        output = getattr(api.Command(), 'gets')('/'.join(endpoint))
    else:
        cloudpoint.run(["plugins", "-h"])
        sys.exit()

    return output


def show(args, endpoint):

    if co.check_attr(args, 'available_plugin_name'):
        endpoint.append(getattr(args, 'available_plugin_name'))

    if (co.check_attr(args, 'plugins_show_command')) and \
       (args.plugins_show_command == "description"):
        if co.check_attr(args, 'available_plugin_name'):
            endpoint.append("description")
        else:
            logger_c.error("'description' requires -i flag for 'PLUGIN_NAME'")
            sys.exit()
    elif (co.check_attr(args, 'plugins_show_command')) and \
         (args.plugins_show_command == "summary"):
        if co.check_attr(args, 'available_plugin_name'):
            logger_c.error("Summary cannot be provided for a specific plugin")
            sys.exit()
        else:
            endpoint.append("summary")


def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format
    print(data)
