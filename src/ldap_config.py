#!/usr/bin/env python3

import sys
import api
import cloudpoint
import logs

LOG_C = logs.setup(__name__, 'c')
LOG_FC = logs.setup(__name__)


def entry_point(args):

    output = None
    endpoint = ['/idm/config/ad']
    if api.check_attr(args, 'ldap_config_command'):
        if args.ldap_config_command == 'show':
            show()
            output = getattr(api.Command(), 'gets')('/'.join(endpoint))

        else:
            LOG_FC.critical("INTERNAL ERROR 1 IN '%s'", __file__)
            sys.exit(1)

    else:
        LOG_C.error("No arguments provided for 'ldap_config'")
        cloudpoint.run(["ldap_config", "-h"])
        sys.exit(1)

    return output


def show():
    # There is no work needed here, since our GETS_DICT provides
    # the whole endpoint ... retaining this for future ?
    pass


def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format
    print(data)
