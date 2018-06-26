#!/usr/bin/env python3

import sys
import constants as co


def roles(args, endpoint):

    if co.check_attr(args, 'role_id'):
        endpoint.append('/' + args.role_id)
    else:
        role_id = input("Enter role id of the role you want to delete : ")
        endpoint.append('/' + role_id)

    return endpoint

def reports(args, endpoint):
    
    report_id = None
    if co.check_attr(args, 'report_id'):
        report_id = '/' + args.report_id
    else:
        report_id = input("Enter the report id you want to delete : ")

    endpoint.append(report_id)

    if co.check_attr(args, 'option'):
        if args.option == 'data':
            endpoint.append('/data')
        elif args.option == 'full':
            pass
        else:
            print("Valid options are 'full' and 'data'\n")
            sys.exit(-1)
    else:
        print("Please provide an option with -o flag\n")
        sys.exit(-2)

    return endpoint
