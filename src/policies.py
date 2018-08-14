#!/usr/bin/env python3

import sys
import api
import cloudpoint
import logs

LOG_C = logs.setup(__name__, 'c')
LOG_FC = logs.setup(__name__)


def entry_point(args):

    endpoint = []
    if args.policies_command == 'asset':
        output = asset(args, endpoint)

    elif args.policies_command == 'create':
        endpoint.append('/policies/')
        data = create()
        print("endpoint is {}\nDATA IS {}".format(endpoint, data))
        output = getattr(api.Command(), 'posts')('/'.join(endpoint), data)

    elif args.policies_command == 'delete':
        endpoint.append('/policies/')
        delete(args, endpoint)
        output = getattr(api.Command(), 'deletes')('/'.join(endpoint))
        print("Delete policy {}\n".format(args.policy_id))

    elif args.policies_command == 'show':
        endpoint.append('/policies/')
        show(args, endpoint)
        output = getattr(api.Command(), 'gets')('/'.join(endpoint))

    else:
        LOG_C.error("No arguments provided for 'policies'")
        cloudpoint.run(["policies", "-h"])
        sys.exit(1)

    return output


def asset(args, endpoint):

    if api.check_attr(args, 'policies_asset_command'):
        endpoint.append('/assets/')
        endpoint.append(args.asset_id)
        endpoint.append('/policies/')
        endpoint.append(args.policy_id)
    else:
        LOG_C.error("No arguments provided for 'asset'")
        cloudpoint.run(["policies", "asset", "-h"])
        sys.exit(1)

    if args.policies_asset_command == 'add':
        output = getattr(api.Command(), 'puts')('/'.join(endpoint), None)

    elif args.policies_asset_command == 'remove':
        output = getattr(api.Command(), 'deletes')('/'.join(endpoint))

    else:
        LOG_FC.critical("INTERNAL ERROR 1 IN '%s'", __file__)
        sys.exit(1)

    return output


def delete(args, endpoint):

    endpoint.append(args.policy_id)


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
        LOG_C.info("Specify Storage/Protection Type. Valid values are %s",
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
        LOG_C.info("Specify schedule type, valid options are %s", sched_types)
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
        LOG_C.info("Enter the retention unit type. Valid values are %s",
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


def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format
    print(data)


def show(args, endpoint):

    if api.check_attr(args, 'policy_id'):
        endpoint.append(args.policy_id)
