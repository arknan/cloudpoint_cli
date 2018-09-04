#!/usr/bin/env python3

import datetime
import json
import sys
import traceback
import texttable
import api
import cloudpoint
import logs
import utils

COLUMNS = utils.get_stty_cols()
LOG_C = logs.setup(__name__, 'c')
LOG_F = logs.setup(__name__, 'f')


def entry_point(args):

    endpoint = []
    output = None
    print_args = None

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
        print_args = show(args, endpoint)
        output = getattr(api.Command(), 'gets')('/'.join(endpoint))

    else:
        LOG_C.error("No arguments provided for 'reports'")
        cloudpoint.run(["reports", "-h"])
        sys.exit(1)

    return output, print_args


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
    if utils.check_attr(args, 'report_id'):
        report_id = '/' + args.report_id
    else:
        report_id = input("Enter the report id you want to delete : ")

    endpoint.append(report_id)

    if not utils.check_attr(args, 'reports_delete_command'):
        endpoint.append('/data')


def re_run(args, endpoint):
    report_id = None
    if utils.check_attr(args, 'report_id'):
        report_id = args.report_id

    else:
        report_id = input("Enter the report id you want to re-run : ")

    endpoint.append(report_id)
    endpoint.append('/data')


def show(args, endpoint):

    print_args = None
    if utils.check_attr(args, 'reports_show_command'):
        if args.reports_show_command == 'report-types':
            if utils.check_attr(args, 'report_id'):
                LOG_C.error("Do not specify a report_id for report-types")
                sys.exit(1)

            endpoint.append('/report-types/')
            print_args = 'report-types'

            if utils.check_attr(args, 'report_type_id'):
                endpoint.append(args.report_type_id)
                print_args = 'report_type_id'

        else:
            endpoint.append('/reports/')
            if utils.check_attr(args, 'report_id'):
                endpoint.append(args.report_id)
                print_args = 'report_id'

            if utils.check_attr(args, 'reports_show_command'):
                if utils.check_attr(args, 'report_id'):
                    if args.reports_show_command == "preview":
                        endpoint.append('/preview')
                        print_args = 'preview'
                    else:
                        endpoint.append('/data')
                        print_args = "data"
                else:
                    LOG_C.error("Specify a REPORT_ID for getting %s",
                                args.reports_show_command)
                    sys.exit(1)
    else:
        endpoint.append('/reports/')
        print_args = "show"
        if utils.check_attr(args, 'report_id'):
            endpoint.append(args.report_id)
            print_args = "report_id"

    return print_args


def pretty_print(output, print_args):

    try:
        table = texttable.Texttable(max_width=COLUMNS)
        pformat = utils.print_format()

        if pformat == 'json':
            print(output)
            sys.exit(0)
        else:
            table.set_deco(pformat)

        if print_args == "report_id":
            data = json.loads(output)
            for k, v in sorted(data.items()):
                if k == 'lastRun':
                    table.add_row((k, datetime.datetime.fromtimestamp(v)))
                elif k == 'columns':
                    table.add_row([k, ', '.join(v)])
                else:
                    table.add_row((k, v))

        elif print_args == 'show':
            data = json.loads(output)
            required = ["reportId", "reportType", "status"]
            table.header([i.capitalize() for i in sorted(required)])
            for i, _ in enumerate(data):
                table.add_row(
                    [v for k, v in sorted(data[i].items()) if k in required])

        elif print_args == 'report-types':
            data = json.loads(output)
            table.header(["ReportType", "Filters"])
            for i, _ in enumerate(data):
                table.add_row((data[i]["reportType"], data[i]['filters']))

        elif print_args == 'report_type_id':
            data = json.loads(output)
            table.header(["Valid Columns", "Valid Column Id's"])
            for i, _ in enumerate(data['columns']):
                vlist = []
                for k, v in sorted(data['columns'][i].items()):
                    vlist.append(v)
                table.add_row(vlist)

        elif print_args in ['preview', 'data']:
            print(output)
            sys.exit(0)

        else:
            data = json.loads(output)
            table.header(("Attribute", "Value"))
            table.add_rows(
                [(k, v) for k, v in sorted(data.items())], header=False)

        if table.draw():
            print(table.draw())

    except(KeyError, AttributeError, TypeError, NameError,
           texttable.ArraySizeError, json.decoder.JSONDecodeError):
        LOG_F.critical(traceback.format_exc())
        print(output)
