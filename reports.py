#!/usr/bin/env python3

import sys
import constants as co
import api

def entry_point(arguments):

    endpoint = ["/reports/"]
    temp = []
    if co.check_attr(arguments, 'reports_command'):
        #temp = arguments.reports_command(arguments, endpoint)
        globals()[arguments.reports_command](arguments, endpoint)
    else:
        print("Internal Error : Invalid function {}".format(arguments.reports_command))

    output = getattr(api.Command(), co.METHOD_DICT[arguments.reports_command])('/'.join(endpoint))
    print(output)

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

