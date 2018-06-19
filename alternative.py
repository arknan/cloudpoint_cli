#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import sys
import argparse
import argcomplete
import api
import show_decider
import create_decider
import modify_decider
import constants as co
from pretty_printer import print_nested as pp


def create_parser():

    parser_main = argparse.ArgumentParser(
        epilog="""
        \n \nFor help information related to each sub-command/positional\
 argument, \nUse "-h" or "--help" at the end of that sub-command \n \n
Examples : "cldpt create -h", \
"cldpt show assets -i <ASSET_ID> --help" \n """,
        formatter_class=argparse.RawTextHelpFormatter)

    subparser_main = parser_main.add_subparsers(dest='command', metavar='<option>')

    parser_show = subparser_main.add_parser("show", help="show operations")
    subparser_show = parser_show.add_subparsers(dest="show_command")

    parser_show_agents = subparser_show.add_parser(
        "agents", help="Get information on agents")
    parser_show_agents.add_argument(
        "-i", "--agent-id", dest="agent_id", metavar="AGENT_ID",
        help="Get information on a specific agent ID")
    subparser_show_agents = parser_show_agents.add_subparsers(dest="agent_command")
    parser_show_agents_plugins = subparser_show_agents.add_parser(
        "plugins", help="Get information on plugins for a specific agent")
    parser_show_agents_plugins.add_argument(
        "-i", "--plugin-name", dest="configured_plugin_name",
        metavar="PLUGIN_NAME",
        help="Get information on a specific plugin name for a specific agent")
    parser_show_agents_summary = subparser_show_agents.add_parser(
        "summary", help="Show summary of agents")

    parser_show_assets = subparser_show.add_parser(
    "assets",help="Get information on assets")
    parser_show_assets.add_argument(
        "-i", "--asset-id", dest="asset_id",
        help="Get information on a specific asset ID")
    subparser_show_assets = parser_show_assets.add_subparsers(dest="asset_command")
    parser_show_assets_snapshots = subparser_show_assets.add_parser(
        "snapshots", help="Get information on snapshots of an asset")
    parser_show_assets_snapshots.add_argument(
        "-i", "--snap-id", dest="snap_id",
        help="Get information on a snapshot ID")
    subparser_show_assets_snapshots =\
    parser_show_assets_snapshots.add_subparsers(dest="snapshot_command")
    parser_show_assets_snapshots_granules = subparser_show_assets_snapshots.add_parser(
        "granules", help = "Get information on granules of asset snapshots")
    parser_show_assets_snapshots_granules.add_argument(
        "-i", "--granule-id", dest="granule_id",
        help="Show information on a particular granule")
    parser_show_assets_policies = subparser_show_assets.add_parser(
        "policies", help="Get information on asset policies")
    parser_show_assets_summary = subparser_show_assets.add_parser(
        "summary", help="Get summary of assets")

    parser_show_licenses = subparser_show.add_parser(
        "licenses", help="Get information on CloudPoint licenses")
    parser_show_licenses.add_argument(
        "-i", "--license-id", dest="license_id", 
        help="Get information on a specific license id")
    subparser_show_licenses = parser_show_licenses.add_subparsers(
        dest="license_command")
    parser_show_licenses_active = subparser_show_licenses.add_parser(
        "active", help="Get information on all active licenses")
    parser_show_licenses_features = subparser_show_licenses.add_parser(
        "features", help="Get information on all licensed features")
    # parser_add("parser_show_join-tokens", ["join-tokens",
    # "Show current join-tokens"])
    parser_show_plugins = subparser_show.add_parser(
        "plugins", help="Get information on available plugins")
    parser_show_plugins.add_argument(
        "-i", "--plugin-name", dest="available_plugin_name",
        metavar="PLUGIN_NAME",
        help="Get information on a specific available plugin")
    subparser_show_plugins = parser_show_plugins.add_subparsers(dest="plugin_command")
    parser_show_plugins_description = subparser_show_plugins.add_parser(
        "description", help="Get plugin description for a specific plugin name")
    parser_show_plugins_description = subparser_show_plugins.add_parser(
        "summary", help="Show summary information for plugins")

    parser_show_policies = subparser_show.add_parser(
        "policies", help="Get information on CloudPoint policies")
    parser_show_policies.add_argument(
        "-i", "--policy-id", help="Get information on a particular policy") 

    parser_show_privileges = subparser_show.add_parser(
        "privileges", help="Get information on privileges")
    parser_show_privileges.add_argument(
        "-i", "--privilege-id",
        help="Get information on a particular privilege")

    parser_show_replication = subparser_show.add_parser(
        "replication", help="Get information on replication rules")

    parser_show_reports = subparser_show.add_parser(
        "reports", help="Get information on reports")
    parser_show_reports.add_argument(
        "-i", "--report-id", dest="report_id",
        help="Get information on a specific report ID")
    subparser_show_reports = parser_show_reports.add_subparsers(dest="report_command")
    parser_show_reports_report_data = subparser_show_reports.add_parser(
        "report-data", help="Show data collected by a specific report") 
    paser_show_reports_preview = subparser_show_reports.add_parser(
        "preview", help="Show first 10 lines of data for a particular report")

    parser_show_roles = subparser_show.add_parser(
        "roles", help="Get information on roles")
    parser_show_roles.add_argument(
        "-i", "--role-id", help="Get information on a specific role ID")
    parser_show_email_config = subparser_show.add_parser(
        "email-config", help="Get information on email server configuration")
    parser_show_ldap_config = subparser_show.add_parser(
        "ldap-config", 
        help="Get information on Active-Directory/LDAP settings")

    parser_show_tags = subparser_show.add_parser(
        "tags", help="Get infomation on classification tags")

    parser_show_tasks = subparser_show.add_parser(
        "tasks", help="Get information on CloudPoint tasks")
    parser_show_tasks.add_argument(
        "-i", "--task-id", help="Get information on a particular task id")
    parser_show_tasks.add_argument(
        "-s", "--status", help="Filter on status, valid values for status are :\
        ['running', 'successful', 'failed']")
    parser_show_tasks.add_argument(
        "-r", "--run-since",
        help="Filter on tasks started in last <RUN_SINCE> no. of hours")
    parser_show_tasks.add_argument(
        "-t", "--taskType", help="Filter on task type, valid values for task \
        types are : ['create-snapshot', 'create-group-snapshot',\
        'delete-snapshot', 'delete-group-snapshots', 'restore']")
    parser_show_tasks.add_argument(
        "-l", "--limit", help="Limit number of results to <LIMIT>")
    subparser_show_tags = parser_show_tags.add_subparsers(dest="tag_command")
    parser_show_tasks_summary = subparser_show_tags.add_parser(
        "summary", help="Get summary information of all tasks")

    parser_show_users = subparser_show.add_parser(
        "users", help="Get information on CloudPoint users")
    parser_show_users.add_argument(
        "-i", "--user-id",
        help="Get information on a particular CloudPoint user")
    parser_show_telemetry = subparser_show.add_parser(
        "telemetry",
        help="Shows CloudPoint's Telemetry status [on/off]")
    parser_show_version = subparser_show.add_parser(
        "version", help="Get CloudPoint's version")

    parser_authenticate = subparser_main.add_parser(
        "authenticate",
        help="Login to CloudPoint ; Required for doing any operation")

    parser_create = subparser_main.add_parser(
        "parser_create", help="Create any information within CloudPoint")
    subparser_create = parser_create.add_subparsers(dest="create_command")
    parser_create_role_assignments = subparser_create.add_parser(
        "role-assignments",
        help="Assign an existing role to an existing user")
    parser_create_email_config = subparser_create.add_parser(
        "email_config", help="Add Email configuration")
    parser_create_user = subparser_create.add_parser(
        "user", help="Create a new user within CloudPoint")
    parser_create_snapshot = subparser_create.add_parser(
        "snapshot", help="Take snapshots of assets")
    parser_create_snapshot.add_argument(
        "-i", "--asset-id", help="Provide an ASSET_ID to snap")

    # parser_add("parser_create_privilege")
    # ("-f", ("--file-name", "JSON formatted file with role details"))})
    parser_modify = subparser_main.add_parser(
        "parser_modify", help="Modify any information within CloudPoint")
    subparser_modify = parser_modify.add_subparsers(dest="modify_command")
    parser_modify_reset_password = subparser_modify.add_parser(
        "reset_password", help="Reset a CloudPoint user's password")

    parser_restore = subparser_main.add_parser(
        "restore", help="Restore snapshots")

    endpoint = []

    if arguments.command == "show":
        if arguments.show_command is None:
            parser_show.print_help()
            sys.exit(100)

        endpoint.append(co.GETS_DICT[arguments.show_command])
        if arguments.show_command in co.COMMON_DECIDER_PATHS:
            endpoint = show_decider.common_paths(endpoint, arguments)
        elif arguments.show_command in co.DECIDER_PATHS:
            endpoint = getattr(
                show_decider, arguments.show_command)(endpoint, arguments)

        print(endpoint)
        return (getattr(api.Command(), co.METHOD_DICT[
            arguments.command])('/'.join(endpoint)), endpoint)

    elif arguments.command == "login":
        getattr(api.Command(), co.METHOD_DICT[arguments.command])()
        sys.exit(4)

    elif arguments.command == "create":
        if arguments.create_command is None:
            parser_create.print_help()
            sys.exit(100)
        # elif arguments.create_command == "role_assignments":
        #    endpoint.append('/authorization/role')
        elif arguments.create_command == "snapshot":
            pass

        elif arguments.create_command in co.POST_DICT:
            endpoint.append(co.POST_DICT[arguments.create_command])
        else:
            print("That is not a valid endpoint to fetch\n")

        data, endpoint = getattr(create_decider, arguments.create_command)(
            arguments, endpoint)

        if arguments.create_command in co.PUTS_LIST:
            return (getattr(api.Command(), "puts")(
                '/'.join(endpoint), data), endpoint)

        return (getattr(api.Command(), co.METHOD_DICT[arguments.command])(
            '/'.join(endpoint), data), endpoint)

    elif arguments.command == "modify":
        if arguments.modify_command is None:
            parser_modify.print_help()
            sys.exit(100)
        elif arguments.modify_command in co.POST_DICT:
            endpoint.append(co.POST_DICT[arguments.modify_command])
        else:
            print("That is not a valid endpoint to fetch\n")

        data = getattr(modify_decider, arguments.modify_command)()

        if arguments.modify_command in co.PUTS_LIST:
            return (getattr(api.Command(), "puts")(
                '/'.join(endpoint), data), endpoint)

    else:
        parser_main.print_help()
        sys.exit(5)


def run(pass_args=None):

    parser = create_parser()
    argcomplete.autocomplete(parser)
    args = parser.parse_args(pass_args)
    if len(pass_args) == 1:
        parser.print_help()
    else:
        output, endpoint = interface(args)
        return output


if __name__ == '__main__':

    parser_main = create_parser()
    argcomplete.autocomplete(parser_main)
    args = parser_main.parse_args(sys.argv[1:])
    if len(sys.argv) == 1:
        parser_main.print_help()
        sys.exit(-1)
    else:
        print(args)
        output, endpoint = interface(args)
        print(output, endpoint)
        pp(output, endpoint)
