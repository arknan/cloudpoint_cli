#!/usr/bin/env python3

import sys
import api
import cloudpoint
import logs

logger_c = logs.setup(__name__, 'c')


def entry_point(args):

    endpoint = ['/telemetry/']

    if args.telemetry_command == 'disable':
        output = getattr(api.Command(), 'deletes')('/'.join(endpoint))

    elif args.telemetry_command == 'enable':
        data = None
        output = getattr(api.Command(), 'posts')('/'.join(endpoint), data)

    elif args.telemetry_command == 'show':
        output = getattr(api.Command(), 'gets')('/'.join(endpoint))

    else:
        logger_c.error("No arguments provided for 'telemetry'\n")
        cloudpoint.run(["telemetry", "-h"])
        sys.exit()

    return output


def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format
    print(data)
