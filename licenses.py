#!/usr/bin/env python3

import sys
import constants as co
import api

def entry_point(args):

    endpoint = []
    endpoint.append(co.GETS_DICT[args.command])
    if co.check_attr(args, 'licenses_command'):
        globals()[args.licenses_command](args, endpoint)
    else:
        print("Invalid argument : '{}'".format(args.licenses_command))
        sys.exit(-1)

    output = getattr(api.Command(), co.METHOD_DICT[args.licenses_command])('/'.join(endpoint))
    # Ideally this is where we would pass the output to a pretty printer function
    print(output)


def show(args, endpoint):

    if co.check_attr(args, 'licenses_show_command'):
        if args.licenses_show_command == "active":
            endpoint.append('/?IsLicenseActive=true')
        elif args.licenses_show_command == "features":
            endpoint.append('/all/features')

    if co.check_attr(args, 'license_id'):
        endpoint.append(getattr(args, 'license_id'))

    return endpoint

