#!/usr/bin/env python3

import sys

EXIT_1 = "\nERROR : Argument 'snapshots' requires -i flag for 'ASSET_ID'\n\
Expected Command Format : cldpt show assets -i <ASSET_ID> snapshots\n"

EXIT_2 = "\nERROR : Granules can only be listed for asset snapshots\n\
Please enter a valid 'SNAP_ID' and 'ASSET_ID'\nExpected Command Format : \
cldpt show assets -i <ASSET_ID> snapshots -i <SNAP_ID> granules\n"

EXIT_5 = "\nERROR : Argument 'plugins' requires -i flag for 'AGENT_ID'\n\
Expected Command Format : cldpt show agents -i <AGENT_ID> plugins\n"

EXIT_6 = "\nERROR:Argument 'description' requires -i flag for 'PLUGIN_NAME'\n\
Expected Command Format : cldpt show plugins -i <PLUGIN_NAME> description\n"


def check_attr(args, attr):

    try:
        if hasattr(args, attr):
            if getattr(args, attr):
                return True
    except NameError:
        return False
    else:
        return False


def common_paths(endpoint, args):

    if args.show_command == "policies":
        detail = "policy_id"
    else :
        detail = (args.show_command)[:-1] + '_id'
    if check_attr(args, detail):
        endpoint.append(getattr(args, detail))

    return endpoint


def assets(endpoint, args):

    if check_attr(args, 'asset_id'):
        endpoint.append(args.asset_id)

    if (check_attr(args, 'assets_command')) and\
       (args.assets_command == "snapshots"):
        if check_attr(args, 'asset_id'):
            endpoint.append(args.assets_command)
            if check_attr(args, 'snapshot_id'):
                endpoint.append(args.snapshot_id)
        else:
            print(EXIT_1)
            sys.exit(2)

        if (check_attr(args, 'snapshots_command')) and\
           (args.snapshots_command == "granules"):
            if (check_attr(args, 'asset_id')) and\
               (check_attr(args, 'snapshot_id')):
                endpoint.append(args.snapshots_command + '/')
                if check_attr(args, 'granule_id'):
                    endpoint.append(args.granule_id)
            else:
                print(EXIT_2)
                sys.exit(3)
    elif (check_attr(args, 'assets_command')) and\
         (args.assets_command == "policies"):
        if check_attr(args, 'asset_id'):
            endpoint.append(args.assets_command)
        else :
            print("\nFor policies, you need to enter an asset_id \n\n")
            sys.exit(4)
    elif (check_attr(args, 'assets_command')) and\
         (args.assets_command == "summary"): 
         if check_attr(args, 'asset_id'):
             print("\nSummary cannot be provided for a specifc asset id\n")
             sys.exit(10)
         else:
             endpoint.append(args.assets_command)

    return endpoint


def agents(endpoint, args):

    detail = (args.show_command)[:-1] + '_id'
    if check_attr(args, detail):
        endpoint.append(getattr(args, detail))

    if (check_attr(args, 'agents_command')) and \
       (args.agents_command == "plugins"):
        if check_attr(args, detail):
            endpoint.append("plugins/")
        else:
            print(EXIT_5)
            sys.exit(101)
        if check_attr(args, "configured_plugin_name"):
            endpoint.append(args.configured_plugin_name)
    elif (check_attr(args, 'agents_command')) and \
         (args.agents_command == "summary"):
         if check_attr(args, detail):
             print("\nSummary cannot be provided for a specific agent\n")
             sys.exit(11)
         else:
             endpoint.append("/summary")

    return endpoint


def plugins(endpoint, args):

    if check_attr(args, 'plugin_name'):
        endpoint.append(getattr(args, 'plugin_name'))

    if (check_attr(args, 'plugins_command')) and \
       (args.plugins_command == "description"):
        if check_attr(args, 'plugin_name'):
            endpoint.append("description")
        else:
            print(EXIT_6)
            sys.exit(102)
    elif (check_attr(args, 'plugins_command')) and \
         (args.plugins_command == "summary"):
         if check_attr(args, 'plugin_name'):
             print("\nSummary cannot be provided for a specific plugin\n")
             sys.exit(12)
         else:
             endpoint.append("/summary")

    return endpoint


def licenses(endpoint, args):

    if check_attr(args, 'licenses_command'):
        if args.licenses_command == "active":
            endpoint.append('/?IsLicenseActive=true')
        elif args.licenses_command == "features":
             endpoint.append('/all/features')

    if check_attr(args, 'license_id'):
        endpoint.append(getattr(args, 'license_id'))


    return endpoint


def tasks(endpoint, args):


    if check_attr(args, 'task_id'):
        if check_attr(args, 'tasks_command'):
            print("\nYou cannot print summary of a task_id\n")
            sys.exit(8)
        endpoint.append(getattr(args, 'task_id'))


    elif check_attr(args, 'tasks_command'):
        endpoint.append('/summary')

    else :
        filters = []
        temp_endpoint = []
        for i in 'run_since', 'limit', 'status', 'taskType' :
            if check_attr(args, i):
                filters.append(i)

        if len(filters) != 0:
            temp_endpoint.append('?' + filters[0] + '=' + getattr(args, filters[0]))
            if len(filters) > 1:
                for j in filters[1:]:
                    temp_endpoint.append('&' + j + '=' + getattr(args, j))
        endpoint.append(''.join(temp_endpoint))

    return endpoint


def reports(endpoint, args):

    if check_attr(args, 'report_id'):
        endpoint.append(getattr(args, 'report_id'))

    if (check_attr(args, 'reports_command')):
        if check_attr(args, 'report_id'):
            if getattr(args, 'reports_command') == "preview":
                endpoint.append('/preview')
            else :
                endpoint.append('/data')
        else:
            print("\nSpecify a REPORT_ID for getting",
                  getattr(args, 'reports_command'), "\n")
            sys.exit(9)

    return endpoint

def settings(endpoint, args):
    if check_attr(args, 'settings_command') :
        if getattr(args, 'settings_command') == "ad" :
            endpoint.append("idm/config/ad")
        elif getattr(args, 'settings_command') == "smtp":
            endpoint.append("email/config")

    return endpoint
