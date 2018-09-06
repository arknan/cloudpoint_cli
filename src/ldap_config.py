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
LOG_FC = logs.setup(__name__)


def entry_point(args):

    endpoint = ['/idm/config/ad']
    output = None
    print_args = None

    if utils.check_attr(args, 'ldap_config_command'):
        if args.ldap_config_command == 'show':
            output = getattr(api.Command(), 'gets')('/'.join(endpoint))

        else:
            LOG_FC.critical("INTERNAL ERROR 1 IN '%s'", __file__)
            sys.exit(1)

    else:
        LOG_C.error("No arguments provided for 'ldap_config'")
        cloudpoint.run(["ldap_config", "-h"])
        sys.exit(1)

    return output, print_args


def show():
    # There is no work needed here, since our GETS_DICT provides
    # the whole endpoint ... retaining this for future ?
    pass


def pretty_print(output, print_args):

    try:
        table = texttable.Texttable(max_width=COLUMNS)
        data = json.loads(output.replace('ldap', ''))
        pformat = utils.print_format()

        if pformat == 'json':
            print(output)
            sys.exit(0)
        else:
            table.set_deco(pformat)

        ignored = ['configKey', 'QueryAttribute']
        table.header([k for k, v in sorted(data.items()) if k not in ignored])
        table.add_row([v for k, v in sorted(data.items()) if k not in ignored])

        if table.draw():
            print(table.draw())

    except(KeyError, AttributeError, TypeError, NameError,
           texttable.ArraySizeError, json.decoder.JSONDecodeError):
        LOG_F.critical(traceback.format_exc())
        print(output)
