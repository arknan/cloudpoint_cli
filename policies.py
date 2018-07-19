#!/usr/bin/env python3

import sys
import api
import cldpt
import constants as co


def entry_point(args):

    endpoint = []
    if args.policies_command == 'asset':
        output = asset(args, endpoint)
    elif args.policies_command == 'create':
        # create(args, endpoint)
        create()
    elif args.policies_command == 'delete':
        delete(args, endpoint)
        output = getattr(api.Command(), 'deletes')('/'.join(endpoint))

    elif args.policies_command == 'show':
        endpoint.append(co.GETS_DICT[args.command])
        show(args, endpoint)
        output = getattr(
            api.Command(), co.METHOD_DICT[args.policies_command])(
                '/'.join(endpoint))
    else:
        print("No arguments provided for 'policies'\n")
        cldpt.run(["policies", "-h"])
        sys.exit(-1)

    return output


def show(args, endpoint):

    if co.check_attr(args, 'policy_id'):
        endpoint.append(args.policy_id)


# def create(args, endpoint):
def create():

    """
    name, appConsist, tag, snapTypePref, hour = None, None, None, None, None
    while True:
        name = input("Policy Name : ")
        if (len(name) > 32) or (len(name) < 2):
            print("Policy Name should be between 2 and 32 characters\n")
        else:
            break
    while True:
        appConsist = (input("Application Consistent ['yes' or 'no'] : ")).lower()
        if appConsist not in ['yes', 'no']:
            print("\nValid options are 'yes' or 'no'\n")
        else:
            if appConsist == 'yes':
                appConsist = True
                break
            else:
                appConsist = False
                break
    tag = input("Description of Policy : ")
    while True:
        snapTypePref = (input("Snapshot type ['cow', 'clone'] : ")).lower()
        if snapTypePref not in ['cow', 'clone']:
            print("\nValid options are 'cow' or 'clone'\n")
        else:
            break

    print("Schedule frequency options, Leave Blank if not applicable :\n")
    minute = input("Minute (0-59): ") or "0"
    hour = input("Hour (0-23): ") or "0"
    month = input("Month : ") or "*"
    wday = input("Day of the week : ") or "*"
    mday = input("Date of the month: ") or "*"

    schedule = {
        "minute": minute,
        "hour": hour,
        "month": month,
        "wday": wday,
        "mday": mday
    }
    """

    print("Not implemented")
    sys.exit()


def asset(args, endpoint):

    if co.check_attr(args, 'policies_asset_command'):
        endpoint.append('/assets/')
        endpoint.append(args.asset_id)
        endpoint.append('/policies/')
        endpoint.append(args.policy_id)
    else:
        print("No arguments provided for 'asset'\n")
        cldpt.run(["policies", "asset", "-h"])
        sys.exit(-1)

    if args.policies_asset_command == 'add':
        output = getattr(api.Command(), 'puts')('/'.join(endpoint), None)

    elif args.policies_asset_command == 'remove':
        output = getattr(api.Command(), 'deletes')('/'.join(endpoint))

    return output

def delete(args, endpoint):
    
    endpoint.append('/policies/')
    endpoint.append(args.policy_id)

def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format
    print(data)
