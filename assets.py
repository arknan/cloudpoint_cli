#!/usr/bin/env python3

import sys
import api
import constants as co

def entry_point(args):

    endpoint = []
    endpoint.append(co.GETS_DICT[args.command])
    if co.check_attr(args, 'assets_command'):
        globals()[args.assets_command](args, endpoint)
    else:
        print("Invalid argument : '{}'".format(args.assets_command))
        sys.exit(-1)

    output = getattr(api.Command(), co.METHOD_DICT[args.assets_command])('/'.join(endpoint))
    # Ideally this is where we would pass the output to a pretty printer function
    print(output)


def show(args, endpoint):

    if co.check_attr(args, 'asset_id'):
        endpoint.append(args.asset_id)

    if (co.check_attr(args, 'assets_show_command')) and\
       (args.assets_show_command == "snapshots"):
        if co.check_attr(args, 'asset_id'):
            endpoint.append(args.assets_show_command)
            if co.check_attr(args, 'snapshot_id'):
                endpoint.append(args.snapshot_id)
        else:
            print(co.EXIT_1)
            sys.exit(2)

        if co.check_attr(args, 'snapshots_command'):
            if args.snapshots_command == "granules":
                if (co.check_attr(args, 'asset_id')) and\
                   (co.check_attr(args, 'snapshot_id')):
                    endpoint.append(args.snapshots_command + '/')
                    if co.check_attr(args, 'granule_id'):
                        endpoint.append(args.granule_id)
                else:
                    print(co.EXIT_2)
                    sys.exit(3)
            elif args.snapshots_command == "restore-targets":
                if (co.check_attr(args, 'asset_id')) and\
                   (co.check_attr(args, 'snapshot_id')):
                    endpoint.append('/targets')
                else:
                    print("Need ASSET_ID and SNAP_ID for restore-targets")
                    sys.exit(-1)

    elif (co.check_attr(args, 'assets_show_command')) and\
         (args.assets_show_command == "policies"):
        if co.check_attr(args, 'asset_id'):
            endpoint.append(args.assets_show_command)
        else:
            print("\nFor policies, you need to enter an asset_id \n\n")
            sys.exit(4)
    elif (co.check_attr(args, 'assets_show_command')) and\
         (args.assets_show_command == "summary"):
        if co.check_attr(args, 'asset_id'):
            print("\nSummary cannot be provided for a specific asset id\n")
            sys.exit(10)
        else:
            endpoint.append(args.assets_show_command)

    return endpoint
