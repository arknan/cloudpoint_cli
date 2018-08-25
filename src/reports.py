#!/usr/bin/env python3

import json
import sys
from texttable import Texttable
import api
import cloudpoint
import logs

LOG_C = logs.setup(__name__, 'c')


def entry_point(args):

    endpoint = []

    if args.reports_command == 'create':
        endpoint.append('/reports/')
        data = create()
        output = getattr(api.Command(), 'posts')('/'.join(endpoint), data)

    elif args.reports_command == 'delete':
        endpoint.append('/reports/')
        delete(args, endpoint)
        output = getattr(api.Command(), 'deletes')('/'.join(endpoint))

    elif args.reports_command == 're_run':
        endpoint.append('/reports/')
        re_run(args, endpoint)
        output = getattr(api.Command(), 'puts')('/'.join(endpoint), None)

    elif args.reports_command == 'show':
        show(args, endpoint)
        output = getattr(api.Command(), 'gets')('/'.join(endpoint))

    else:
        LOG_C.error("No arguments provided for 'reports'")
        cloudpoint.run(["reports", "-h"])
        sys.exit(1)

    return output


def create():

    valid_cols = [
        "classification", "replicas", "sourceName", "consistent", "createdBy",
        "snapType", "id", "ctime", "name", "region", "provider"]

    report_id = input("Report Name : ")

    # Defaulting report_type to 'snapshot' since there are no other types
    # As of CP 2.0.2
    report_type = 'snapshot'
    LOG_C.info("Enter a comma separated list of Report fields/columns")
    LOG_C.info("Valid values are : %s\n", sorted(valid_cols))
    given_cols = (input("Report Columns :\n")).replace(' ', '').split(',')

    for col_type in given_cols:
        if col_type not in valid_cols:
            LOG_C.error("'%s' isn't a valid column type.\nValid types are %s",
                        col_type, valid_cols)
            sys.exit(1)

    expiry_days = input("Report Expiry (in days): ")
    expiry = 86400 * int(expiry_days)
    data = {
        "reportId": report_id,
        "reportType": report_type,
        "columns": given_cols,
        "expire": expiry
    }

    return data


def delete(args, endpoint):

    report_id = None
    if api.check_attr(args, 'report_id'):
        report_id = '/' + args.report_id
    else:
        report_id = input("Enter the report id you want to delete : ")

    endpoint.append(report_id)

    if not api.check_attr(args, 'reports_delete_command'):
        endpoint.append('/data')


def re_run(args, endpoint):
    report_id = None
    if api.check_attr(args, 'report_id'):
        report_id = args.report_id

    else:
        report_id = input("Enter the report id you want to re-run : ")

    endpoint.append(report_id)
    endpoint.append('/data')


def show(args, endpoint):

    if api.check_attr(args, 'reports_show_command'):
        if args.reports_show_command == 'report-types':
            endpoint.append('/report-types/')

        else:
            endpoint.append('/reports/')
            if api.check_attr(args, 'report_id'):
                endpoint.append(args.report_id)

            if api.check_attr(args, 'reports_show_command'):
                if api.check_attr(args, 'report_id'):
                    if args.reports_show_command == "preview":
                        endpoint.append('/preview')
                    else:
                        endpoint.append('/data')
                else:
                    LOG_C.error("Specify a REPORT_ID for getting %s",
                                args.reports_show_command)
                    sys.exit(1)
    else:
        endpoint.append('/reports/')
        if api.check_attr(args, 'report_id'):
            endpoint.append(args.report_id)


def pretty_print(args, output):
    print(output)
