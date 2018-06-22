#!/usr/bin/env python3

import sys
import constants as co


def common_paths(endpoint, args):

    if args.show_command == "policies":
        detail = "policy_id"
    else:
        detail = (args.show_command)[:-1] + '_id'
    if co.check_attr(args, detail):
        endpoint.append(getattr(args, detail))

    return endpoint


def assets(endpoint, args):

    if co.check_attr(args, 'asset_id'):
        endpoint.append(args.asset_id)

    if (co.check_attr(args, 'assets_command')) and\
       (args.assets_command == "snapshots"):
        if co.check_attr(args, 'asset_id'):
            endpoint.append(args.assets_command)
            if co.check_attr(args, 'snapshot_id'):
                endpoint.append(args.snapshot_id)
        else:
            print(co.EXIT_1)
            sys.exit(2)

        if co.check_attr(args, 'snapshots_command'):
            if args.snapshots_command == "granules":
                if (co.check_attr(args, 'asset_id')) and\
                   (co.check_attr(args, 'snapshot_id')):
                    endpoint.append(args.snapshots_command + '/')
                    if co.check_attr(args, 'granule_id'):
                        endpoint.append(args.granule_id)
                else:
                    print(co.EXIT_2)
                    sys.exit(3)
            elif args.snapshots_command == "restore-targets":
                if (co.check_attr(args, 'asset_id')) and\
                   (co.check_attr(args, 'snapshot_id')):
                   endpoint.append('/targets')
                else:
                    print("Need ASSET_ID and SNAP_ID for restore-targets")
                    sys.exit(-1)


    elif (co.check_attr(args, 'assets_command')) and\
         (args.assets_command == "policies"):
        if co.check_attr(args, 'asset_id'):
            endpoint.append(args.assets_command)
        else:
            print("\nFor policies, you need to enter an asset_id \n\n")
            sys.exit(4)
    elif (co.check_attr(args, 'assets_command')) and\
         (args.assets_command == "summary"):
        if co.check_attr(args, 'asset_id'):
            print("\nSummary cannot be provided for a specifc asset id\n")
            sys.exit(10)
        else:
            endpoint.append(args.assets_command)

    return endpoint


def agents(endpoint, args):

    detail = (args.show_command)[:-1] + '_id'
    if co.check_attr(args, detail):
        endpoint.append(getattr(args, detail))

    if (co.check_attr(args, 'agents_command')) and \
       (args.agents_command == "plugins"):
        if co.check_attr(args, detail):
            endpoint.append("plugins/")
        else:
            print(co.EXIT_5)
            sys.exit(101)
        if co.check_attr(args, "configured_plugin_name"):
            endpoint.append(args.configured_plugin_name)
    elif (co.check_attr(args, 'agents_command')) and \
         (args.agents_command == "summary"):
        if co.check_attr(args, detail):
            print("\nSummary cannot be provided for a specific agent\n")
            sys.exit(11)
        else:
            endpoint.append("summary")

    return endpoint


def plugins(endpoint, args):

    if co.check_attr(args, 'plugin_name'):
        endpoint.append(getattr(args, 'plugin_name'))

    if (co.check_attr(args, 'plugins_command')) and \
       (args.plugins_command == "description"):
        if co.check_attr(args, 'plugin_name'):
            endpoint.append("description")
        else:
            print(co.EXIT_6)
            sys.exit(102)
    elif (co.check_attr(args, 'plugins_command')) and \
         (args.plugins_command == "summary"):
        if co.check_attr(args, 'plugin_name'):
            print("\nSummary cannot be provided for a specific plugin\n")
            sys.exit(12)
        else:
            endpoint.append("summary")

    return endpoint


def licenses(endpoint, args):

    if co.check_attr(args, 'licenses_command'):
        if args.licenses_command == "active":
            endpoint.append('/?IsLicenseActive=true')
        elif args.licenses_command == "features":
            endpoint.append('/all/features')

    if co.check_attr(args, 'license_id'):
        endpoint.append(getattr(args, 'license_id'))

    return endpoint


def tasks(endpoint, args):

    if co.check_attr(args, 'task_id'):
        if co.check_attr(args, 'tasks_command'):
            print("\nYou cannot print summary of a task_id\n")
            sys.exit(8)
        endpoint.append(getattr(args, 'task_id'))

    elif co.check_attr(args, 'tasks_command'):
        endpoint.append('/summary')

    else:
        filters = []
        temp_endpoint = []
        for i in 'run_since', 'limit', 'status', 'taskType':
            if co.check_attr(args, i):
                filters.append(i)

        if (len(filters) != 0) and (filters[0]):
            temp_endpoint.append('?' + filters[0] + '=' +
                                 getattr(args, filters[0]))
            if len(filters) > 1:
                for j in filters[1:]:
                    temp_endpoint.append('&' + j + '=' + getattr(args, j))
        endpoint.append(''.join(temp_endpoint))

    return endpoint


def reports(endpoint, args):

    if co.check_attr(args, 'report_id'):
        endpoint.append(getattr(args, 'report_id'))

    if co.check_attr(args, 'reports_command'):
        if co.check_attr(args, 'report_id'):
            if getattr(args, 'reports_command') == "preview":
                endpoint.append('/preview')
            else:
                endpoint.append('/data')
        else:
            print("\nSpecify a REPORT_ID for getting",
                  getattr(args, 'reports_command'), "\n")
            sys.exit(9)

    return endpoint


def settings(endpoint, args):

    if co.check_attr(args, 'settings_command'):
        if getattr(args, 'settings_command') == "ad":
            endpoint.append("idm/config/ad")
        elif getattr(args, 'settings_command') == "smtp":
            endpoint.append("email/config")

    return endpoint

def replication(endpoint, args):
    
    if co.check_attr(args, 'policy_name'):
        endpoint.append(getattr(args, 'policy_name'))
    if co.check_attr(args, 'replication_command'):
        if co.check_attr(args, 'policy_name'):
            endpoint.append('/rules/')
        else:
            print("Mention a policy name to get replication rules\n")
            sys.exit(-1)

    return endpoint
