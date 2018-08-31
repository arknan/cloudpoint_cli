#!/usr/bin/env python3

import datetime
import json
import sys
import texttable
import api
import cloudpoint
import logs
import utils

COLUMNS = utils.get_stty_cols()
LOG_C = logs.setup(__name__, 'c')
LOG_FC = logs.setup(__name__)


def entry_point(args):

    endpoint = ['/assets/']

    if args.assets_command == "create-snapshot":
        data = create_snapshot(args, endpoint)
        output = getattr(api.Command(), 'posts')('/'.join(endpoint), data)
        pretty_print(output, "create-snapshot")

    elif args.assets_command == "delete-snapshot":
        output = delete_snapshot(args, endpoint)
        pretty_print(output, "delete-snapshot")

    elif args.assets_command == "policy":
        output = policy(args, endpoint)
        pretty_print(output, "policy")

    elif args.assets_command == 'replicate':
        data = replicate(args, endpoint)
        output = getattr(api.Command(), 'posts')('/'.join(endpoint), data)
        pretty_print(output, "replicate")

    elif args.assets_command == "restore":
        data = restore(args)
        output = getattr(api.Command(), 'puts')('/'.join(endpoint), data)
        pretty_print(output, "restore")

    elif args.assets_command == "show":
        print_args = show(args, endpoint)
        output = getattr(api.Command(), 'gets')('/'.join(endpoint))
        pretty_print(output, print_args)

    else:
        LOG_C.error("No arguments provided for 'assets'")
        cloudpoint.run(["assets", "-h"])
        sys.exit(1)


def create_snapshot(args, endpoint):
    if utils.check_attr(args, "asset_id"):
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

    if utils.check_attr(args, 'snapshot_id') and \
       utils.check_attr(args, 'file_name'):
        LOG_C.error("Either provide %s or %s, not both", "snapshot_id",
                    "file_name")
        sys.exit(1)

    output = None
    if utils.check_attr(args, 'snapshot_id'):
        if del_snap(args.snapshot_id, endpoint):
            output = getattr(api.Command(), "deletes")('/'.join(endpoint))
        else:
            LOG_C.error("%s not a valid snapshot_id", args.snapshot_id)
            output = ""

        return output

    else:
        file_input = None
        if utils.check_attr(args, 'file_name'):
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
                pretty_print(args, output)

        return "\n"


def policy(args, endpoint):

    if utils.check_attr(args, 'assets_policy_command'):
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

    if not utils.check_attr(args, "snapshot_id"):
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

    print_args = None
    if utils.check_attr(args, 'asset_id'):
        endpoint.append(args.asset_id)
        print_args = "asset_id"

        if utils.check_attr(args, 'assets_show_command'):
            if args.assets_show_command == "snapshots":
                endpoint.append("/snapshots")
                print_args = "snapshots"

                if utils.check_attr(args, 'snapshot_id'):
                    endpoint.append(args.snapshot_id)
                    print_args = "snapshot_id"

                    if utils.check_attr(args, 'snapshots_command'):
                        if args.snapshots_command == "granules":
                            endpoint.append(args.snapshots_command + '/')
                            print_args = "granules"

                            if utils.check_attr(args, 'granule_id'):
                                endpoint.append(args.granule_id)
                                print_args = "granule_id"

                        elif args.snapshots_command == "restore-targets":
                            endpoint.append('/targets')
                            print_args = "restore-targets"

                        else:
                            LOG_FC.critical(
                                "INTERNAL ERROR 2 IN %s", __file__)
                            sys.exit(1)

            elif args.assets_show_command == "policies":
                endpoint.append("/policies/")
                print_args = "policies"

    else:
        print_args = "show"
        if utils.check_attr(args, 'assets_show_command'):
            if args.assets_show_command in ['snapshots', 'policies']:
                LOG_C.error("Argument '%s' needs an asset_id",
                            args.assets_show_command)
                sys.exit(1)

            elif args.assets_show_command == "summary":
                endpoint.append('/summary')
                print_args = "summary"
            else:
                LOG_FC.critical("INTERNAL ERROR 3 IN '%s'", __file__)
                sys.exit(1)

    return print_args

def replicate(args, endpoint):

    snap_id = None
    if utils.check_attr(args, 'snapshot_id'):
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


def pretty_print(output, print_args):

    try:
        table = texttable.Texttable(max_width=COLUMNS)
        table.set_deco(texttable.Texttable.HEADER)

        if print_args == "asset_id":
            data = json.loads(output)
            ignore = ['parentId', 'snapMethods', 'plugin', '_links',
                      'protectionLevels', 'actions']

            table.add_rows(
                [(k, v) for k, v in sorted(data.items()) if k not in ignore],
                header=False)

        elif print_args == "show":
            data = json.loads(output)['items']
            required = ["id", "type", "location"]
            table.header(sorted(required))

            for i, _ in enumerate(data):
                if data[i]['type'] in ['disk', 'host', "filesystem", "application"]:
                    table.add_row([
                        v for k, v in sorted(data[i].items()) if k in required
                        ])

        elif print_args == "snapshots":
            
            data = json.loads(output)['items']
            required = ["id", "ctime", "type"]
            table.header(sorted(required))

            for i, _ in enumerate(data):
                vlist = []
                for k, v in sorted(data[i].items()):
                    if k in required:
                        if k == 'ctime':
                            vlist.append(datetime.datetime.fromtimestamp(v))
                        elif k == 'type':
                            vlist.append(v.split(':')[0])
                        else:
                            vlist.append(v)
                table.add_row([i for i in vlist])

        elif print_args == "snapshot_id":
            data = json.loads(output)
            ignored = ["_links", "actions"]
            vlist = []
            klist = []
            for k, v in sorted(data.items()):
                if k not in ignored:
                    klist.append(k)
                    if k == "ctime":
                        vlist.append(datetime.datetime.fromtimestamp(v))
                    elif k == "attachment":
                        vlist.append((data[k].values()))
                    else:
                        vlist.append(v)

                    if klist and vlist:
                        table.add_row([klist.pop(), vlist.pop()])

        elif print_args == "granules":
            data = json.loads(output)["items"]
            required = ["id", "name"]
            table.header(sorted(required))
            for i, _ in enumerate(data):
                table.add_row([v for k, v in sorted(data[i].items()) if k in required])

        elif print_args == "granule_id":
            data = json.loads(output)
            table.add_rows([(k, v) for k, v in sorted(data.items())], header=False)

        else:
            data = json.loads(output)
            table.add_rows(
                [(k, v) for k, v in sorted(data.items())], header=False)

        if table.draw():
            print(table.draw())

    except(KeyError, AttributeError, TypeError, NameError,
           texttable.ArraySizeError, json.decoder.JSONDecodeError):
        print(output)
