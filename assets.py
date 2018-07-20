#!/usr/bin/env python3

import json
import sys
import api
import cldpt
import constants as co


def entry_point(args):

    endpoint = ['/assets/']

    if args.assets_command == "policy":
        output = policy(args, endpoint)

    elif args.assets_command == "create":
        data = create(args, endpoint)
        output = getattr(api.Command(), co.METHOD_DICT['create'])(
            '/'.join(endpoint), data)

    elif args.assets_command == "delete-snapshot":
        delete(args, endpoint)
        output = getattr(api.Command(), "deletes")('/'.join(endpoint))

    elif args.assets_command == "restore":
        data = restore(args, endpoint)
        output = getattr(api.Command(), "puts")('/'.join(endpoint), data)

    elif args.assets_command == "show":
        show(args, endpoint)
        output = getattr(api.Command(), co.METHOD_DICT[args.assets_command])(
            '/'.join(endpoint))

    else:
        print("No arguments provided for 'assets'\n")
        cldpt.run(["assets", "-h"])
        sys.exit(-1)

    return output


def create(args, endpoint):
    data = None
    if co.check_attr(args, 'assets_create_command'):
        if args.assets_create_command == 'snapshot':
            data = create_snapshot(args, endpoint)
        elif args.assets_create_command == 'replica':
            data = create_replica(endpoint)
    else:
        print("No arguments provided for 'create'\n")
        cldpt.run(["assets", "create", "-h"])
        sys.exit(-1)

    return data


def create_replica(endpoint):

    print("\nEnter the snapshot ID to replicate and the destination(s)\n")
    print("A maximum of 3 destinations are allowed\n")
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

    print("Valid destination regions are : {}".format(valid_locations))

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
            print("\nNot a valid location\n")
            print("Valid destination regions are : {}".format(valid_locations))

    if not dest:
        print("\nYou should provide atleast 1 region to replicate to !\n")
        sys.exit(-1)

    data = {
        "snapType": "replica",
        "srcSnapId": snap_id,
        "dest": dest
    }
    endpoint.append(snap_source_asset)
    endpoint.append('/snapshots/')

    return data


def create_snapshot(args, endpoint):
    if co.check_attr(args, "asset_id"):
        endpoint.append(args.asset_id)
        endpoint.append('/snapshots/')
    else:
        print("\nPlease mention an ASSET_ID for taking snapshot\n")
        sys.exit(-1)

    snap_types = json.loads(cldpt.run(
        ["assets", "show", "-i", args.asset_id]))["snapMethods"]
    print("\nPlease enter a snapshot type")
    print("Valid types for this asset include :", snap_types)
    snap_type = input("SnapType : ")
    snap_name = input("Snapshot Name : ")
    snap_descr = input("Description : ")
    snap_bool = None
    while True:
        snap_bool = input("Consistent ? [True / False] : ")
        if snap_bool in ["True", "False"]:
            break
        else:
            print("\nChoose either 'True' or 'False'\n")
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

    if co.check_attr(args, 'assets_policy_command'):
        endpoint.append(args.asset_id)
        endpoint.append('/policies/')
        endpoint.append(args.policy_id)
    else:
        print("No arguments provided for 'policy'\n")
        cldpt.run(["assets", "policy", "-h"])
        sys.exit(-1)

    if args.assets_policy_command == 'assign':
        output = getattr(api.Command(), 'puts')('/'.join(endpoint), None)

    elif args.assets_policy_command == 'remove':
        output = getattr(api.Command(), 'deletes')('/'.join(endpoint))

    return output


def restore(args, endpoint):

    if not co.check_attr(args, "snapshot_id"):
        print("\nPlease mention a SNAP_ID for doing restores\n")
        sys.exit(-1)

    print("\nPlease enter a restore location type.\n")
    print("Valid values are [new, original]\n")
    restore_loc = None
    data = {
        "snapid": args.snapshot_id
    }
    while True:
        restore_loc = input("Restore Location : ")
        if restore_loc in ['new', 'original']:
            break
    if restore_loc == 'new':
        # endpoint.append("/" + args.snapshot_id)
        snap_info = json.loads(getattr(api.Command(), 'gets')(
            '/assets/' + args.snapshot_id))
        snap_source_id = snap_info["snapSourceId"]
        snap_type = snap_info["attachment"]["type"]
        if snap_type == 'host':
            data["dest"] = snap_source_id
        else:
            print("\nSnapshot type is : ", snap_type)
            print("\nOnly host type snapshots are supported thru CLI\n")
    else:
        print("INTERNAL ERROR")
        sys.exit(-1)

    return data


def show(args, endpoint):

    if co.check_attr(args, 'asset_id'):
        endpoint.append(args.asset_id)
        if co.check_attr(args, 'assets_show_command'):
            if args.assets_show_command == "snapshots":
                endpoint.append(args.assets_show_command)
                if co.check_attr(args, 'snapshot_id'):
                    endpoint.append(args.snapshot_id)
                    if co.check_attr(args, 'snapshots_command'):
                        if args.snapshots_command == "granules":
                            endpoint.append(args.snapshots_command + '/')
                            if co.check_attr(args, 'granule_id'):
                                endpoint.append(args.granule_id)
                        elif args.snapshots_command == "restore-targets":
                            endpoint.append('/targets')
                        else:
                            print("INTERNAL ERROR")
                            sys.exit()
                else:
                    print("Argument '{}' needs a snapshot_id".format(
                        args.snapshots_command))
                    sys.exit()

            elif args.assets_show_command == "policies":
                endpoint.append(args.assets_show_command)

    else:
        if args.assets_show_command in ['snapshots', 'policies']:
            print("Argument '{}' needs an asset_id".format(
                args.assets_show_command))
            sys.exit()
        if co.check_attr(args, 'assets_show_command'):
            if args.assets_show_command == "summary":
                endpoint.append('/summary')
            elif args.assets_show_command == "all":
                pass
            else:
                print("INTERNAL ERROR")
                sys.exit()
        else:
            endpoint.append('/?limit=3')
            print("\nBY DEFAULT ONLY 3 ASSETS ARE SHOWN")
            print("TO SEE THE ALL ASSETS, RUN : 'cldpt assets show all'\n")


def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format
    print(data)
