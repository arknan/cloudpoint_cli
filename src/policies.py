#!/usr/bin/env python3

import json
import re
import sys
from texttable import Texttable
import api
import cloudpoint
import logs

LOG_C = logs.setup(__name__, 'c')
LOG_FC = logs.setup(__name__)


def entry_point(args):

    endpoint = []
    if args.policies_command == 'asset':
        output = asset(args)

    elif args.policies_command == 'create':
        endpoint.append('/policies/')
        data = create()
        print("endpoint is {}\nDATA IS {}".format(endpoint, data))
        output = getattr(api.Command(), 'posts')('/'.join(endpoint), data)

    elif args.policies_command == 'delete':
        endpoint.append('/policies/')
        pol_id, pol_nm = delete(args, endpoint)
        output = getattr(api.Command(), 'deletes')('/'.join(endpoint))
        print("Deleted policy {} : ({})\n".format(pol_nm, pol_id))

    elif args.policies_command == 'show':
        endpoint.append('/policies/')
        show(args, endpoint)
        output = getattr(api.Command(), 'gets')('/'.join(endpoint))

    else:
        LOG_C.error("No arguments provided for 'policies'")
        cloudpoint.run(["policies", "-h"])
        sys.exit(1)

    return output


def asset(args):

    output = None

    def abstractor(ast_id, cmd, pl_id):
        out = None
        tmp_endpoint = []
        tmp_endpoint.append('/assets/')
        tmp_endpoint.append(ast_id)
        tmp_endpoint.append('/policies/')
        tmp_endpoint.append(pl_id)
        if cmd == 'add':
            out = getattr(api.Command(), 'puts')('/'.join(tmp_endpoint), None)

        elif cmd == 'remove':
            out = getattr(api.Command(), 'deletes')('/'.join(tmp_endpoint))

        else:
            LOG_FC.critical("INTERNAL ERROR 1 IN '%s'", __file__)
            sys.exit(1)

        return out

    def validate_policy(args):

        if api.check_attr(args, 'policy_id'):
            pol_id = args.policy_id
        elif api.check_attr(args, 'policy_name'):
            pol_id = pol_name_to_id(args.policy_name)
        else:
            LOG_C.error("Either provide %s or %s\n",
                        "policy_id", "policy_name")
            cloudpoint.run(["policies", "asset", "-h"])
            sys.exit(1)

        return pol_id

    if api.check_attr(args, 'policies_asset_command'):
        if api.check_attr(args, 'asset_id'):
            if api.check_attr(args, 'policy_id') and \
               api.check_attr(args, 'policy_name'):
                LOG_C.error("Either provide %s or %s, not both",
                            "policy_id", "policy_name")
                sys.exit(1)

            pol_id = validate_policy(args)
            output = abstractor(args.asset_id, args.policies_asset_command,
                                pol_id)

        elif api.check_attr(args, 'file_name'):
            try:
                with open(args.file_name, 'r') as infile:
                    file_input = infile.readlines()

            except FileNotFoundError as fnfe:
                LOG_C.error("Please check if file %s exists", args.file_name)
                LOG_C.info(fnfe)
                sys.exit(1)

            pol_id = validate_policy(args)

            for lines in file_input:
                line = lines.strip().replace('\"', '')
                ret_val = abstractor(line, args.policies_asset_command, pol_id)
                LOG_C.info(ret_val)

            output = "\n"

        else:
            LOG_C.error("Either provide %s or %s\n",
                        "asset_id", "file_name containing asset id's")
            sys.exit(1)

    else:
        LOG_C.error("No arguments provided for 'asset'")
        cloudpoint.run(["policies", "asset", "-h"])
        sys.exit(1)

    return output


def delete(args, endpoint):

    pol_id = None
    pol_nm = None
    if api.check_attr(args, 'policy_id') and \
       api.check_attr(args, 'policy_name'):
        LOG_C.error("Either provide %s or %s, not both",
                    "policy_id", "policy_name")
        sys.exit(1)

    if api.check_attr(args, 'policy_id'):
        pol_id = args.policy_id
        pol_nm = pol_id_to_name(pol_id)
        if not pol_nm:
            LOG_C.error("Invalid policy '%s'\n", args.policy_id)
            sys.exit(1)

    elif api.check_attr(args, 'policy_name'):
        pol_nm = args.policy_name
        pol_id = pol_name_to_id(pol_nm)
        if not pol_id:
            LOG_C.error("Invalid policy '%s'\n", args.policy_name)
            sys.exit(1)

    else:
        LOG_C.error("Either provide %s or %s", "policy_id", "policy_name")
        sys.exit(1)

    endpoint.append(pol_id)
    return (pol_id, pol_nm)


def create():

    name = None
    while True:
        name = input("Policy Name : ")
        if (len(name) > 32) or (len(name) < 2):
            LOG_C.error(
                "Policy Name should be between 2 and 32 characters\n")
        else:
            break

    app_consist = True
    while True:
        app_consist = (input(
            "Application Consistent ['y' or 'n'] (y) : ")).lower() or 'y'
        if app_consist not in ['y', 'n']:
            LOG_C.error("Valid options are 'y' or 'n'\n")
        else:
            if app_consist == 'y':
                app_consist = True
                break
            else:
                app_consist = False
                break

    tag = input("Description of Policy : ") or ""

    prot_level = None
    prot_levels = ['disk', 'host', 'application']

    while True:
        LOG_C.info("Specify Storage/Protection Type. Valid values are\n%s",
                   prot_levels)
        prot_level = input("Protection Type : ")
        if prot_level in prot_levels:
            break
        else:
            LOG_C.error("Invalid Protection Type '%s'\n", prot_level)

    replica = False
    while True:
        replica = (
            input("Replicate Snapshot ['y' or 'n'] (n) : ")).lower() or 'n'
        if replica == 'y':
            replica = True
            break
        elif replica == 'n':
            replica = False
            break
        else:
            LOG_C.error("Invalid Value. Valid options are 'y' OR 'n'\n")

    sched_types = ['minutes', 'hourly', 'daily', 'weekly', 'monthly']
    sched_type = None
    while True:
        LOG_C.info("Specify schedule type, valid options are\n%s", sched_types)
        sched_type = input("Schedule Type : ")
        if sched_type not in sched_types:
            LOG_C.info("'%s' Not a valid schedule type\n", sched_type)
        else:
            break

    minute = "0"
    hour = "0"
    month = "*"
    wday = "*"
    mday = "*"
    valid_wkdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                    'saturday', 'sunday']

    if sched_type == 'minutes':
        while True:
            LOG_C.info("Snapshot every _ minutes? Valid range:%s", '[0-59]')
            minute = input("minutes : ")
            if minute in str(list(range(60))):
                break
            else:
                LOG_C.error("Invalid Value '%s'\n", minute)

    elif sched_type == 'hourly':
        while True:
            LOG_C.info("Snapshot every _ hours? Valid range:%s", '[0-23]')
            hour = input("hour : ")
            if hour in str(list(range(24))):
                break
            else:
                LOG_C.error("Invalid Value '%s'\n", hour)

    elif sched_type == 'daily':
        while True:
            LOG_C.info("Snapshot every day at _ ? Valid range:%s", '[0-23]')
            hour = input("hour (0): ") or "0"
            if hour in str(list(range(24))):
                break
            else:
                LOG_C.error("Invalid Value '%s'\n", hour)

    elif sched_type == 'weekly':
        while True:
            LOG_C.info("Snapshot every week on _ ? Valid values:%s",
                       valid_wkdays)
            wday = input("Day of the week : ")
            if wday in valid_wkdays:
                while True:
                    LOG_C.info("Snapshot at _ ? Valid range:%s", '[0-23]')
                    hour = input("hour (0): ") or "0"
                    if hour in str(list(range(24))):
                        break
                    else:
                        LOG_C.error("Invalid Value '%s'\n", hour)
                break
            else:
                LOG_C.error("Invalid Value '%s'\n", wday)

    else:
        while True:
            LOG_C.info("Snapshot every month on _ ? Valid values:%s",
                       '[1-31]')
            mday = input("Date : ")
            if mday in str(list(range(1, 32))):
                while True:
                    LOG_C.info("Snapshot at _ ? Valid range:%s", '[0-23]')
                    hour = input("hour (0): ") or "0"
                    if hour in str(list(range(24))):
                        break
                    else:
                        LOG_C.error("Invalid Value '%s'\n", hour)
                break
            else:
                LOG_C.error("Invalid Value '%s'\n", mday)

    schedule = {
        "minute": minute,
        "hour": hour,
        "month": month,
        "wday": wday,
        "mday": mday
    }

    ret_unit_types = ['snapshots', 'days', 'weeks', 'months', 'years']
    ret_unit_type = None
    while True:
        LOG_C.info("Enter the retention unit type. Valid values are\n%s",
                   ret_unit_types)
        ret_unit_type = input("Retention unit type : ")
        if ret_unit_type in ret_unit_types:
            break

    ret_val = int(input("Retention Value : "))

    retention = {
        "unit": ret_unit_type,
        "value": ret_val
    }

    data = {
        "name": name,
        "tag": tag,
        "protectionLevel": prot_level,
        "replicate": replica,
        "appConsist": app_consist,
        "retention": retention,
        "schedule": schedule
    }

    return data


def show(args, endpoint):

    if api.check_attr(args, 'policies_show_command'):

        if api.check_attr(args, 'policy_id') or \
           api.check_attr(args, 'policy_name'):
            LOG_C.error("protected-assets subcommand doesn't take \
policy_id argument")
            sys.exit(1)

        if args.policies_show_command == 'protected-assets':
            if api.check_attr(args, 'policies_show_protected_assets_command'):
                data = protected_assets(ast_only=1)
                pretty_print("protected_assets_1", data)

            else:
                data = protected_assets(ast_only=0)
                pretty_print("protected_assets_0", data)

        else:
            data = unprotected_assets()
            pretty_print("unprotected_assets", data)

        sys.exit(0)

    if api.check_attr(args, 'policy_id') and \
       api.check_attr(args, 'policy_name'):
        LOG_C.error("Either provide %s or %s, not both",
                    "policy_id", "policy_name")
        sys.exit(1)

    if api.check_attr(args, 'policy_id'):
        endpoint.append(args.policy_id)
    else:
        if api.check_attr(args, 'policy_name'):
            pol_id = pol_name_to_id(args.policy_name)
            endpoint.append(pol_id)


def pol_map():

    policy_list = cloudpoint.run(["policies", "show"])
    matches = re.findall(r'"id":(.*),\s+\n\s+"name":(.*),\s+', policy_list)

    return matches


def pol_id_to_name(pol_id):
    pl_nm = None
    match = pol_map()
    pol_dict = {json.loads(i[0]): json.loads(i[1]) for i in match}

    try:
        pl_nm = pol_dict[pol_id]
    except KeyError:
        pass

    return pl_nm


def pol_name_to_id(pol_name):

    pl_id = None
    match = pol_map()
    pol_dict = {json.loads(i[1]): json.loads(i[0]) for i in match}

    try:
        pl_id = pol_dict[pol_name]
    except KeyError:
        LOG_C.error("Invalid policy name : '%s'", pol_name)
        sys.exit(1)

    return pl_id


def protected_assets(ast_only=0):

    prot_ast = {}
    assets_only = []
    all_pols = json.loads(cloudpoint.run(["policies", "show"]))
    ret_val = None

    if ast_only == 0:
        prot_ast = {
            all_pols[i]['name']: all_pols[i]['assets']
            for i, _ in enumerate(all_pols)}

        ret_val = prot_ast

    else:
        for i, _ in enumerate(all_pols):
            for j in all_pols[i]['assets']:
                assets_only.append(j)

        ret_val = assets_only

    return ret_val


def unprotected_assets():
    all_asset_list = []
    prot_asset_list = protected_assets(ast_only=1)
    all_assets = json.loads(cloudpoint.run(["assets", "show"]))['items']

    tmp = []
    for i, _ in enumerate(all_assets):
        for key, value in sorted(all_assets[i].items()):
            if key in ['id', 'type']:
                tmp.append(value)

    tmp_len = len(tmp)
    if tmp_len % 2 != 0:
        LOG_FC.error("INTERNAL ERROR 2 IN '%s'", __file__)
        sys.exit(1)

    for i in range(0, tmp_len, 2):
        if tmp[i+1] in ["disk", "host"]:
            all_asset_list.append((tmp[i]).strip().replace('"', ''))

    unprot_asset_list = list(set(all_asset_list).difference(prot_asset_list))

    return unprot_asset_list


def pretty_print(args, output):

    table = Texttable()
    if args == "protected_assets_0":
        table.add_rows([(k, v) for k, v in sorted(output.items())],
                       header=False)
        print(table.draw())
        sys.exit()

    elif args == "protected_assets_1":
        table.header(["PROTECTED ASSETS"])
        for i in output:
            table.add_row([i])
        print(table.draw())
        sys.exit()

    elif args == "unprotected_assets":
        table.header(["UNPROTECTED ASSETS"])
        for i in output:
            table.add_row([i])
        print(table.draw())
        sys.exit()

    data = json.loads(output)

    if api.check_attr(args, 'policy_id') or \
       api.check_attr(args, 'policy_name'):
        for k, v in sorted(data.items()):
            if isinstance(v, dict):
                table.add_row([k, sorted(v.items())])
            else:
                table.add_row([k, v])

    else:
        required = ["name", "id"]
        table.header(sorted(required))
        for i, _ in enumerate(data):
            table.add_row(
                [v for k, v in sorted(data[i].items()) if k in required])

    print(table.draw())
