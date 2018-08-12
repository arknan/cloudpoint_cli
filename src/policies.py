#!/usr/bin/env python3

import sys
import api
import cloudpoint
import logs

logger_c = logs.setup(__name__, 'c')
logger_fc = logs.setup(__name__)


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
        logger_c.error("No arguments provided for 'policies'")
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
        logger_c.error("No arguments provided for 'asset'")
        cloudpoint.run(["policies", "asset", "-h"])
        sys.exit(1)

    if args.policies_asset_command == 'add':
        output = getattr(api.Command(), 'puts')('/'.join(endpoint), None)

    elif args.policies_asset_command == 'remove':
        output = getattr(api.Command(), 'deletes')('/'.join(endpoint))

    else:
        logger_fc.critical("INTERNAL ERROR 1 IN '%s'", __file__)
        sys.exit(1)

    return output


def delete(args, endpoint):

    endpoint.append(args.policy_id)


def create():

    name = None
    while True:
        name = input("Policy Name : ")
        if (len(name) > 32) or (len(name) < 2):
            logger_c.error(
                "Policy Name should be between 2 and 32 characters\n")
        else:
            break

    appConsist = True
    while True:
        appConsist = (input(
            "Application Consistent ['y' or 'n'] (y) : ")).lower() or 'y'
        if appConsist not in ['y', 'n']:
            logger_c.error("Valid options are 'y' or 'n'\n")
        else:
            if appConsist == 'y':
                appConsist = True
                break
            else:
                appConsist = False
                break

    tag = input("Description of Policy : ") or ""

    prot_level = None
    prot_levels = ['disk', 'host', 'application']

    while True:
        logger_c.info("Specify Storage/Protection Type. Valid values are %s",
                      prot_levels)
        prot_level = input("Protection Type : ")
        if prot_level in prot_levels:
            break
        else:
            logger_c.error("Invalid Protection Type '%s'\n", prot_level)

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
            logger_c.error("Invalid Value. Valid options are 'y' OR 'n'\n")

    sched_types = ['minutes', 'hourly', 'daily', 'weekly', 'monthly']
    sched_type = None
    while True:
        logger_c.info("Specify schedule type, valid options are %s", sched_types)
        sched_type = input("Schedule Type : ")
        if sched_type not in sched_types:
            logger_c.info("'%s' Not a valid schedule type\n", sched_type)
        else:
            break

    minute = "0"
    hour = "0"
    month =  "*"
    wday = "*"
    mday = "*"
    valid_wkdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                    'saturday', 'sunday']

    if sched_type == 'minutes':
        while True:
            logger_c.info("Snapshot every _ minutes? Valid range:%s", '[0-59]')
            minute = input("minutes : ")
            if minute in str(list(range(60))):
                break
            else:
                logger_c.error("Invalid Value '%s'\n", minute)

    elif sched_type == 'hourly':
        while True:
            logger_c.info("Snapshot every _ hours? Valid range:%s", '[0-23]')
            hour = input("hour : ")
            if hour in str(list(range(24))):
                break
            else:
                logger_c.error("Invalid Value '%s'\n", hour)

    elif sched_type == 'daily':
        while True:
            logger_c.info("Snapshot every day at _ ? Valid range:%s", '[0-23]')
            hour = input("hour (0): ") or "0"
            if hour in str(list(range(24))):
                break
            else:
                logger_c.error("Invalid Value '%s'\n", hour)

    elif sched_type == 'weekly':
        while True:
            logger_c.info("Snapshot every week on _ ? Valid values:%s",
                          valid_wkdays)
            wday = input("Day of the week : ")
            if wday in valid_wkdays:
                while True:
                    logger_c.info("Snapshot at _ ? Valid range:%s", '[0-23]')
                    hour = input("hour (0): ") or "0"
                    if hour in str(list(range(24))):
                        break
                    else:
                        logger_c.error("Invalid Value '%s'\n", hour)
                break
            else:
                logger_c.error("Invalid Value '%s'\n", wday)

    else:
        while True:
            logger_c.info("Snapshot every month on _ ? Valid values:%s",
                          '[1-31]')
            mday = input("Date : ")
            if mday in str(list(range(1, 32))):
                while True:
                    logger_c.info("Snapshot at _ ? Valid range:%s", '[0-23]')
                    hour = input("hour (0): ") or "0"
                    if hour in str(list(range(24))):
                        break
                    else:
                        logger_c.error("Invalid Value '%s'\n", hour)
                break
            else:
                logger_c.error("Invalid Value '%s'\n", mday)


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
        logger_c.info("Enter the retention unit type. Valid values are %s",
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
        "appConsist": appConsist,
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


