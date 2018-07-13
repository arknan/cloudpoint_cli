#!/usr/bin/env python3

import sys
import api
import constants as co

def entry_point(args):

    endpoint = []
    endpoint.append(co.GETS_DICT[args.command])
    if co.check_attr(args, 'reports_command'):
        globals()[args.reports_command](args, endpoint)
    else:
        print("Invalid argument : '{}'".format(args.reports_command))
        sys.exit(-1)

    output = getattr(api.Command(), co.METHOD_DICT[args.reports_command])('/'.join(endpoint))
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

    return endpoint

# TO DO : add create method and other methods as needed

def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format that makes parsing easier !
    print(data)
