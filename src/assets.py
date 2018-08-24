#!/usr/bin/env python3

import json
import sys
from texttable import Texttable
from pprint import pprint
import api
import cloudpoint
import logs

LOG_C = logs.setup(__name__, 'c')
LOG_FC = logs.setup(__name__)


def entry_point(args):

    endpoint = ['/assets/']

    if args.assets_command == "create-snapshot":
        data = create_snapshot(args, endpoint)
        output = getattr(api.Command(), 'posts')('/'.join(endpoint), data)

    elif args.assets_command == "delete-snapshot":
        output = delete_snapshot(args, endpoint)

    elif args.assets_command == "policy":
        output = policy(args, endpoint)

    elif args.assets_command == 'replicate':
        data = replicate(args, endpoint)
        output = getattr(api.Command(), 'posts')('/'.join(endpoint), data)

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


def create_snapshot(args, endpoint):
    if api.check_attr(args, "asset_id"):
        endpoint.append(args.asset_id)
        endpoint.append('/snapshots/')
    else:
        LOG_C.error("Please mention an ASSET_ID for taking snapshot")
        sys.exit(1)

    # The GUI asks only 2 questions, hence commenting out the complexities
    # More questions can always be asked ;)
    """
    snap_types = json.loads(cloudpoint.run(
        ["assets", "show", "-i", args.asset_id]))["snapMethods"]
    LOG_C.info("Please enter a snapshot type")
    LOG_C.info("Valid types for this asset include :%s", snap_types)
    snap_type = input("SnapType : ")
    """
    snap_name = input("Snapshot Name : ")
    snap_descr = input("Description : ")
    """
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
    """
    data = {
        "name": snap_name,
        "description": snap_descr
    }

    return data


def delete_snapshot(args, endpoint):

    def del_snap(snap_id, tmp_endpt):

        err = True
        snap_info = json.loads(cloudpoint.run(
            ['assets', 'show', '-i', snap_id]))
        try:
            snap_source_asset = snap_info["snapSourceId"]
            tmp_endpt.append(snap_source_asset)
            tmp_endpt.append('/snapshots/')
            tmp_endpt.append(snap_id)
        except KeyError:
            err = False

        return err

    if api.check_attr(args, 'snapshot_id') and \
       api.check_attr(args, 'file_name'):
        LOG_C.error("Either provide %s or %s, not both", "snapshot_id",
                    "file_name")
        sys.exit(1)

    output = None
    if api.check_attr(args, 'snapshot_id'):
        if del_snap(args.snapshot_id, endpoint):
            output = getattr(api.Command(), "deletes")('/'.join(endpoint))
        else:
            LOG_C.error("%s not a valid snapshot_id", args.snapshot_id)
            output = ""

        return output

    else:
        file_input = None
        if api.check_attr(args, 'file_name'):
            try:
                with open(args.file_name, 'r') as infile:
                    file_input = infile.readlines()
            except FileNotFoundError as fnfe:
                LOG_C.error("Please check if file %s exists", args.file_name)
                LOG_C.info(fnfe)
                sys.exit(1)

        for snap_ids in file_input:
            snap_id = snap_ids.strip().replace('\"', '')
            output = cloudpoint.run(
                ['assets', 'delete-snapshot', '-i', snap_id])
            if output:
                pretty_print(output)

        return "\n"


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
                endpoint.append("/snapshots")

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

            elif args.assets_show_command == "policies":
                endpoint.append("/policies/")

            elif args.assets_show_command == "all":
                LOG_C.error("'all' sub-command doesn't work with an asset_id")
                sys.exit(1)

    else:
        if api.check_attr(args, 'assets_show_command'):
            if args.assets_show_command in ['snapshots', 'policies']:
                LOG_C.error("Argument '%s' needs an asset_id",
                            args.assets_show_command)
                sys.exit(1)

            elif args.assets_show_command == "summary":
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


def replicate(args, endpoint):

    snap_id = None
    if api.check_attr(args, 'snapshot_id'):
        snap_id = args.snapshot_id
    else:
        LOG_C.info("Enter the snapshot ID to replicate and the destination(s)")
        snap_id = input("Snapshot ID : ")

    LOG_C.info("A maximum of 3 destinations are allowed for replication\n")
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


def pretty_print(args, output):

    def cleanse(data, req_fields):
        for k in list(data.keys()):
            if k not in req_fields:
                del data[k]

    table = Texttable()

    if api.check_attr(args, 'asset_id'):
        data = json.loads(output)
        ignore = ['parentId', 'snapMethods', 'plugin', '_links',
                         'protectionLevels', 'actions']
        required_fields = [k for k, v in data.items() if k not in ignore]
        cleanse(data, required_fields)
        table.add_rows(list((k, v) for k, v in sorted(data.items())), header=False)

    else:
        print_fields = ["id", "type", "location"]
        data = json.loads(output)['items']
        table.header(sorted(print_fields))

        for i, _ in enumerate(data):
            if data[i]['type'] in ['disk', 'host']:
                cleanse(data[i], print_fields)
                table.add_row(list(v for k, v in sorted(data[i].items()) if k in print_fields))

    print(table.draw())
