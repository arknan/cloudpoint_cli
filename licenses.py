#!/usr/bin/env python3

import sys
import api
import constants as co

def entry_point(args):

    endpoint = []
    if args.licenses_command == 'show':
        endpoint.append(co.GETS_DICT[args.command])
        show(args, endpoint)
        output = getattr(api.Command(), co.METHOD_DICT[args.licenses_command])('/'.join(endpoint))
    else:
        print("Invalid argument : '{}'".format(args.licenses_command))
        sys.exit(-1)

    return output

def show(args, endpoint):

    if co.check_attr(args, 'licenses_show_command'):
        if args.licenses_show_command == "active":
            endpoint.append('/?IsLicenseActive=true')
        elif args.licenses_show_command == "features":
            endpoint.append('/all/features')

    if co.check_attr(args, 'license_id'):
        endpoint.append(getattr(args, 'license_id'))

def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format that makes parsing easier !
    print(data)
