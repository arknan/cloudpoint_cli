#!/usr/bin/env python3

import sys
import api
import constants as co

def entry_point(args):

    endpoint = []
    if args.reports_command == 'show':
        endpoint.append(co.GETS_DICT[args.command])
        show(args, endpoint)
        output = getattr(api.Command(), co.METHOD_DICT[args.reports_command])('/'.join(endpoint))

    elif args.reports_command == 'create':
        create(args, endpoint)

    else:
        print("Invalid argument : '{}'".format(args.reports_command))
        sys.exit(-1)

    return output

def show(args, endpoint):

    if co.check_attr(args, 'report_id'):
        endpoint.append(getattr(args, 'report_id'))

    if co.check_attr(args, 'reports_show_command'):
        if co.check_attr(args, 'report_id'):
            if getattr(args, 'reports_show_command') == "preview":
                endpoint.append('/preview')
            else:
                endpoint.append('/data')
        else:
            print("\nSpecify a REPORT_ID for getting",
                  getattr(args, 'reports_show_command'), "\n")
            sys.exit(9)

def create(args, endpoint):


    """
    report_id = input("Report Name : ")
    first_name = input("Firstname : ")
    last_name = input("Lastname : ")
    email_addr = input("Email : ")
    data = {
        "lastName": last_name,
        "email": email_addr,
        "firstName": first_name
    }
    return (data, endpoint)
    """
    print("Not implemented")
    sys.exit(-1)

def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format that makes parsing easier !
    print(data)
