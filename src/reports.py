#!/usr/bin/env python3

import sys
import api
import cloudpoint
import constants as co
import logs

logger_c = logs.setup(__name__, 'c')


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
        logger_c.error("No arguments provided for 'reports'")
        cloudpoint.run(["reports", "-h"])
        sys.exit()

    return output


def create():

    valid_cols = [
        "classification", "replicas", "sourceName", "consistent", "createdBy",
        "snapType", "id", "ctime", "name", "region", "provider"]

    report_id = input("Report Name : ")

    # Defaulting report_type to 'snapshot' since there are no other types
    # As of CP 2.0.2
    report_type = 'snapshot'
    logger_c.info("Enter a comma separated list of Report fields/columns")
    logger_c.info("Valid values are : ", sorted(valid_cols), "\n")
    given_cols = (input("Report Columns :\n")).replace(' ', '').split(',')

    for col_type in given_cols:
        if col_type not in valid_cols:
            logger_c.error("{} is not a valid column type.\nValid types are {}".format(
                col_type, valid_cols))
            sys.exit()

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
    if co.check_attr(args, 'report_id'):
        report_id = '/' + args.report_id
    else:
        report_id = input("Enter the report id you want to delete : ")

    endpoint.append(report_id)

    if not co.check_attr(args, 'reports_delete_command'):
        endpoint.append('/data')


def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format
    print(data)


def re_run(args, endpoint):
    report_id = None
    if co.check_attr(args, 'report_id'):
        report_id = args.report_id

    else:
        report_id = input("Enter the report id you want to re-run : ")

    endpoint.append(report_id)
    endpoint.append('/data')


def show(args, endpoint):

    if co.check_attr(args, 'reports_show_command'):
        if args.reports_show_command == 'report-types':
            endpoint.append('/report-types/')

        else:
            endpoint.append('/reports/')
            if co.check_attr(args, 'report_id'):
                endpoint.append(args.report_id)

            if co.check_attr(args, 'reports_show_command'):
                if co.check_attr(args, 'report_id'):
                    if args.reports_show_command == "preview":
                        endpoint.append('/preview')
                    else:
                        endpoint.append('/data')
                else:
                    logger_c.error("Specify a REPORT_ID for getting {}".format(
                        args.reports_show_command))
                    sys.exit()
    else:
        endpoint.append('/reports/')
        if co.check_attr(args, 'report_id'):
            endpoint.append(args.report_id)
