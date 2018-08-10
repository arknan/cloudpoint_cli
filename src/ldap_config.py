#!/usr/bin/env python3

import sys
import api
import cloudpoint


def entry_point(args):

    endpoint = ['/idm/config/ad']
    if args.ldap_config_command == 'show':
        show()
        output = getattr(api.Command(), 'gets')('/'.join(endpoint))

    else:
        cloudpoint.run(["ldap_config", "-h"])
        sys.exit()

    return output


def show():
    # There is no work needed here, since our GETS_DICT provides
    # the whole endpoint ... retaining this for future ?
    pass


def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format
    print(data)
