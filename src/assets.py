#!/usr/bin/env python3

import json
import sys
import api
import cloudpoint
import logs

LOG_C = logs.setup(__name__, 'c')
LOG_FC = logs.setup(__name__)


def entry_point(args):

    endpoint = ['/assets/']

    if args.assets_command == "create":
        data = create(args, endpoint)
        output = getattr(api.Command(), 'posts')('/'.join(endpoint), data)

    elif args.assets_command == "delete-snapshot":
        delete(args, endpoint)
        output = getattr(api.Command(), "deletes")('/'.join(endpoint))

    elif args.assets_command == "policy":
        output = policy(args, endpoint)

    elif args.assets_command == "restore":
        data = restore(args)
        output = getattr(api.Command(), 'puts')('/'.join(endpoint), data)

    elif args.assets_command == "show":
        show(args, endpoint)
        output = getattr(api.Command(), 'gets')('/'.join(endpoint))

    else:
        LOG_C.error("No arguments provided for 'assets'")
        cloudpoint.run(["assets", "-h"])
        sys.exit(1)

    return output


def create(args, endpoint):
    data = None
    if api.check_attr(args, 'assets_create_command'):
        if args.assets_create_command == 'snapshot':
            data = create_snapshot(args, endpoint)
        elif args.assets_create_command == 'replica':
            data = create_replica(endpoint)
    else:
        LOG_C.error("No arguments provided for 'create'")
        cloudpoint.run(["assets", "create", "-h"])
        sys.exit(1)

    return data


def create_replica(endpoint):

    LOG_C.info("Enter the snapshot ID to replicate and the destination(s)")
    LOG_C.info("A maximum of 3 destinations are allowed\n")
    snap_id = input("Snapshot ID : ")

    snap_info = json.loads(getattr(api.Command(), 'gets')(
        '/assets/' + snap_id))
    snap_source_asset = snap_info["snapSourceId"]
    repl_locations = json.loads(getattr(api.Command(), 'gets')(
        '/assets/' + snap_source_asset + '/snapshots/' + snap_id +
        '/repl-targets/'))

    valid_locations = []
    for i in repl_locations:
        valid_locations.append(i["region"])

    LOG_C.info("Valid destination regions are : %s", valid_locations)

    dest_counter = 0
    dest = []
    while dest_counter < 3:
        temp = input("Destination (enter 'none' if you are done) : ")
        if temp == 'none':
            break

        elif temp in valid_locations:
            for i in repl_locations:
                if temp == i["region"]:
                    dest.append(i["id"])
                    dest_counter += 1

        else:
            LOG_C.error("\nNot a valid location\n")
            LOG_C.info(
                "Valid destination regions are : %s}", valid_locations)

    if not dest:
        LOG_C.error("You should provide atleast 1 region to replicate to !")
        sys.exit(1)

    data = {
        "snapType": "replica",
        "srcSnapId": snap_id,
        "dest": dest
    }
    endpoint.append(snap_source_asset)
    endpoint.append('/snapshots/')

    return data


def create_snapshot(args, endpoint):
    if api.check_attr(args, "asset_id"):
        endpoint.append(args.asset_id)
        endpoint.append('/snapshots/')
    else:
        LOG_C.error("Please mention an ASSET_ID for taking snapshot")
        sys.exit(1)

    snap_types = json.loads(cloudpoint.run(
        ["assets", "show", "-i", args.asset_id]))["snapMethods"]
    LOG_C.info("Please enter a snapshot type")
    LOG_C.info("Valid types for this asset include :%s", snap_types)
    snap_type = input("SnapType : ")
    snap_name = input("Snapshot Name : ")
    snap_descr = input("Description : ")
    snap_bool = None
    while True:
        snap_bool = input("Consistent ? [True / False] : ")
        if snap_bool in ["True", "False"]:
            break
        else:
            LOG_C.error("Choose either 'True' or 'False'")
    data = {
        "snapType": snap_type,
        "name": snap_name,
        "description": snap_descr,
        "consistent": snap_bool
    }

    return data


def delete(args, endpoint):

    snap_info = json.loads(getattr(api.Command(), 'gets')(
        '/assets/' + args.snapshot_id))
    snap_source_asset = snap_info["snapSourceId"]
    endpoint.append('/assets/')
    endpoint.append(snap_source_asset)
    endpoint.append('/snapshots/')
    endpoint.append(args.snapshot_id)


def policy(args, endpoint):

    if api.check_attr(args, 'assets_policy_command'):
        endpoint.append(args.asset_id)
        endpoint.append('/policies/')
        endpoint.append(args.policy_id)
    else:
        LOG_C.error("No arguments provided for 'policy'")
        cloudpoint.run(["assets", "policy", "-h"])
        sys.exit(1)

    if args.assets_policy_command == 'assign':
        output = getattr(api.Command(), 'puts')('/'.join(endpoint), None)

    elif args.assets_policy_command == 'remove':
        output = getattr(api.Command(), 'deletes')('/'.join(endpoint))

    return output


def restore(args):

    if not api.check_attr(args, "snapshot_id"):
        LOG_C.error("Please mention a SNAP_ID for doing restores")
        sys.exit(1)

    LOG_C.info("\nPlease enter a restore location type.\n")
    LOG_C.info("Valid values are [new, original]\n")
    restore_loc = None
    data = {
        "snapid": args.snapshot_id
    }
    while True:
        restore_loc = input("Restore Location : ")
        if restore_loc in ['new', 'original']:
            break
    if restore_loc == 'new':
        snap_info = json.loads(getattr(api.Command(), 'gets')(
            '/assets/' + args.snapshot_id))
        snap_source_id = snap_info["snapSourceId"]
        snap_type = snap_info["attachment"]["type"]
        if snap_type == 'host':
            data["dest"] = snap_source_id
        else:
            LOG_C.info("Snapshot type is : %s", snap_type)
            LOG_C.error("Only host type snapshots are supported thru CLI")
    else:
        LOG_FC.critical("INTERNAL ERROR 1 IN %s", __file__)
        sys.exit(1)

    return data


def show(args, endpoint):

    if api.check_attr(args, 'asset_id'):
        endpoint.append(args.asset_id)
        if api.check_attr(args, 'assets_show_command'):
            if args.assets_show_command == "snapshots":
                endpoint.append(args.assets_show_command)
                if api.check_attr(args, 'snapshot_id'):
                    endpoint.append(args.snapshot_id)
                    if api.check_attr(args, 'snapshots_command'):
                        if args.snapshots_command == "granules":
                            endpoint.append(args.snapshots_command + '/')
                            if api.check_attr(args, 'granule_id'):
                                endpoint.append(args.granule_id)
                        elif args.snapshots_command == "restore-targets":
                            endpoint.append('/targets')
                        else:
                            LOG_FC.critical(
                                "INTERNAL ERROR 2 IN %s", __file__)
                            sys.exit(1)
                else:
                    LOG_C.error("Argument '%s' needs a snapshot_id",
                                args.snapshots_command)
                    sys.exit(1)

            elif args.assets_show_command == "policies":
                endpoint.append(args.assets_show_command)

    else:
        if args.assets_show_command in ['snapshots', 'policies']:
            LOG_C.error("Argument '%s' needs an asset_id",
                        args.assets_show_command)
            sys.exit(1)

        if api.check_attr(args, 'assets_show_command'):
            if args.assets_show_command == "summary":
                endpoint.append('/summary')
            elif args.assets_show_command == "all":
                pass
            else:
                LOG_FC.critical("INTERNAL ERROR 3 IN '%s'", __file__)
                sys.exit(1)
        else:
            endpoint.append('/?limit=3')
            LOG_C.info("BY DEFAULT ONLY 3 ASSETS ARE SHOWN")
            LOG_C.info("TO SEE ALL ASSETS : 'cloudpoint assets show all'")


def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format
    print(data)
