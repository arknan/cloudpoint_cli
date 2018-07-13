#!/usr/bin/env python3

import sys
import api
import constants as co

def entry_point(args):

    endpoint = []
    if args.policies_command == 'show':
        endpoint.append(co.GETS_DICT[args.command])
        show(args, endpoint)
        output = getattr(api.Command(), co.METHOD_DICT[args.policies_command])('/'.join(endpoint))
    elif args.policies_command == 'create':
        create(args, endpoint)
    else:
        print("Invalid argument : '{}'".format(args.policies_command))
        sys.exit(-1)

    return output

def show(args, endpoint):
    
    if co.check_attr(args, 'policy_id'):
        endpoint.append(args.policy_id)

def create(args, endpoint):

    """
    name, appConsist, tag, snapTypePref, hour = None, None, None, None, None
    schedule = {}
    print(name, appConsist, tag, snapTypePref, hour, schedule)
    while True:
        name = input("Policy Name : ")
        if (len(name) > 32) or (len(name) < 2):
            print("Policy Name should be between 2 and 32 characters\n")
        else:
            break
    while True:
        appConsist = input("Application Consistent ['True' or 'False'] : ")
        if appConsist not in ['True', 'False']:
            print("\nValid options are 'True' or 'False'\n")
        else:
            if appConsist == 'True':
                appConsist = True
                break
            else:
                appConsist = False
                break
    tag = input("Description of Policy : ")
    while True:
        snapTypePref = input("Snapshot type ['cow', 'clone'] : ")
        if snapTypePref not in ['cow', 'clone']:
            print("\nValid options are 'cow' or 'clone'\n")
        else:
            break
    sched_dict = {
        'minute': 'Backup every __ minute(s) :',
        'hour' : 'Backup every __ hour(s) :',
        'day': 'Backup on __day :',
    print("Schedule frequency options, Leave Blank if not applicable :\n")
    freq = input(
        "Backup every \n['minute', 'hour', 'day', 'week', 'month', 'year']\n
        Frequency : ")
    minute = input("Minute : ") or "0"
    hour = input("Hour : ") or "0"
    mday = input("Date : ") or "1"
    month = input("Month : ") or "1"
    wday = input("Day of the week : ")
    mday = input("Date of the month: ")
    """
    print("Not implemented")
    sys.exit(-1)


def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format that makes parsing easier !
    print(data)
