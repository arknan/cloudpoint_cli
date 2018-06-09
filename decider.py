#!/usr/bin/env python3

import sys

EXIT_1 = "\nERROR : Argument 'snapshots' requires -i flag for 'ASSET_ID'\n\
Expected Command Format : cldpt show assets -i <ASSET_ID> snapshots\n"

EXIT_2 = "\nERROR : Granules can only be listed for asset snapshots\n\
Please enter a valid 'SNAP_ID' and 'ASSET_ID'\nExpected Command Format : \
cldpt show assets -i <ASSET_ID> snapshots -i <SNAP_ID> granules\n"

EXIT_5 = "\nERROR : Argument 'plugins' requires -i flag for 'AGENT_ID'\n\
Expected Command Format : cldpt show agents -i <AGENT_ID> plugins\n"

EXIT_6 = "\nERROR:Argument 'description' requires -i flag for 'PLUGIN_NAME'\n\
Expected Command Format : cldpt show plugins -i <PLUGIN_NAME> description\n"


def check_attr(args, attr):

    try:
        if hasattr(args, attr):
            if getattr(args, attr):
                return True
    except NameError:
        return False
    else:
        return False


def common_paths(endpoint, args):

    detail = (args.show_command)[:-1] + '_id'
    if check_attr(args, detail):
        endpoint.append(getattr(args, detail))

    return endpoint


def assets(endpoint, args):

    if check_attr(args, 'asset_id'):
        endpoint.append(args.asset_id)

    if (check_attr(args, 'assets_command')) and\
       (args.assets_command == "snapshots"):
        if check_attr(args, 'asset_id'):
            endpoint.append(args.assets_command)
            if check_attr(args, 'snapshot_id'):
                endpoint.append(args.snapshot_id)
        else:
            print(EXIT_1)
            sys.exit(2)

        if (check_attr(args, 'snapshots_command')) and\
           (args.snapshots_command == "granules"):
            if (check_attr(args, 'asset_id')) and\
               (check_attr(args, 'snapshot_id')):
                endpoint.append(args.snapshots_command + '/')
                if check_attr(args, 'granule_id'):
                    endpoint.append(args.granule_id)
            else:
                print(EXIT_2)
                sys.exit(3)

    return endpoint


def agents(endpoint, args):

    detail = (args.show_command)[:-1] + '_id'
    if check_attr(args, detail):
        endpoint.append(getattr(args, detail))

    if (check_attr(args, 'agents_command')) and \
       (args.agents_command == "plugins"):
        if check_attr(args, detail):
            endpoint.append("plugins/")
        else:
            print(EXIT_5)
            sys.exit(101)
        if check_attr(args, "configured_plugin_name"):
            endpoint.append(args.configured_plugin_name)

    return endpoint


def plugins(endpoint, args):

    if check_attr(args, 'plugin_name'):
        endpoint.append(getattr(args, 'plugin_name'))

    if (check_attr(args, 'plugins_command')) and \
       (args.plugins_command == "description"):
        if check_attr(args, 'plugin_name'):
            endpoint.append("description")
        else:
            print(EXIT_6)
            sys.exit(102)

    return endpoint
