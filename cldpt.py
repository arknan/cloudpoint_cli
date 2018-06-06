#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import sys
import argparse
import argcomplete
import api
import decider

GETS_DICT = {
    "ad-config": "idm/config/ad",
    "agents": "agents/",
    "assets": "assets/",
    "classification-tags": "classifications/tags",
    "email-config": "email/config",
    "granules": "granules",
    "jointokens": "jointokens/",
    "licenses": "licenses/",
    "plugins": "plugins/",
    "policies": "policies/",
    "privileges": "/authorization/privilege/",
    "replication": "replication/",
    "report-types": "report-types/",
    "reports": "reports/",
    "roles": "authorization/role",
    "schedules": "schedules/",
    "tasks": "tasks/",
    "telemetry": "telemetry/",
    "users": "idm/user/",
    "version": "version"
}

METHOD_DICT = {
    "show": "gets",
    "create": "posts",
    "authenticate": "authenticate"
}

EXIT_1 = "\nERROR : Argument 'snapshots' requires -i flag for 'ASSET_ID'\n\
Expected Command Format : cldpt show assets -i <ASSET_ID> snapshots\n"

EXIT_2 = "\nERROR : Granules can only be listed for asset snapshots\n\
Please enter a valid 'SNAP_ID' and 'ASSET_ID'\nExpected Command Format : \
cldpt show assets -i <ASSET_ID> snapshots -i <SNAP_ID> granules\n"

EXIT_3 = "\nERROR : Unknown option passed\n"

EXIT_4 = "\nERROR : You need to provide an argument to SHOW\n\
Expected Command Format : cldpt show assets ; cldpt show reports\n"

EXIT_5 = "\nERROR : Argument 'plugins' requires -i flag for 'AGENT_ID'\n\
Expected Command Format : cldpt show agents -i <AGENT_ID> plugins\n"


def create_parser():

    parser_main = \
        argparse.ArgumentParser(epilog="""\n \nFor help information\
 related to each sub-command/positional argument, \nUse "-h" or "--help"\
 at the end of that sub-command \n \nExamples : "cldpt create -h",\
 "cldpt show assets -i <ASSET_ID> --help" \n """,
                                formatter_class=argparse.RawTextHelpFormatter)
    subparser_main = parser_main.add_subparsers(dest='command')

    parser_show = subparser_main.add_parser("show", help="show operations")
    subparser_show = parser_show.add_subparsers(dest="sub_command")

    parser_show_reports = subparser_show.add_parser("reports",
        help="Get information on reports")
    parser_show_reports.add_argument("-i", "--report-id", dest="report_id",
        help="Get information on a specific report ID")

    parser_show_assets = subparser_show.add_parser("assets",
        help="Get information on assets")
    parser_show_assets.add_argument("-i", "--asset-id", dest="asset_id",
        help="Get information on a specific asset ID")

    subparser_show_assets = parser_show_assets.add_subparsers(dest="asset_command")
    parser_show_assets_snapshots = subparser_show_assets.add_parser("snapshots",
        help="Get information on snapshots of an asset")
    parser_show_assets_snapshots.add_argument("-i", "--snap-id", dest="snap_id",
        help="Get information on a snapshot ID")

    subparser_show_assets_snapshots =\
        parser_show_assets_snapshots.add_subparsers(dest="snapshot_command")
    parser_show_assets_snapshots_granules =\
        subparser_show_assets_snapshots.add_parser("granules",
        help="Get information on granules for a snapshot of an asset")
    parser_show_assets_snapshots_granules.add_argument("-i", "--granule-id", dest="granule_id",
        help="Get information on a specific granule for a specific snapshot")

    parser_show_privileges = subparser_show.add_parser("privileges",
        help="Get information on privileges")
    parser_show_privileges.add_argument("-i", "--privilege-id", dest="privilege_id",
        help="Get information on a specific privilege ID")

    parser_show_roles = subparser_show.add_parser("roles",
        help="Get information on roles")
    parser_show_roles.add_argument("-i", "--role-id", dest="role_id",
        help="Get information on a specific role ID")

    parser_show_email_config = subparser_show.add_parser("email-config",
         help="Get information on email server configuration")
    parser_show_users = subparser_show.add_parser("users",
        help="Get information on users")
    parser_show_users.add_argument("-i", "--user-id", dest="user_id",
        help="Get information on a specific user ID")

    parser_show_agents = subparser_show.add_parser("agents",
        help="Get information on agents")
    parser_show_agents.add_argument("-i", "--agent-id", dest="agent_id",
        help="Get information on a specific agent ID")
    subparser_show_agents = parser_show_agents.add_subparsers(dest="agent_command")
    parser_show_agents_plugins = subparser_show_agents.add_parser("plugins",
        help="Get information on plugins for a specific agent")
    parser_show_agents_plugins.add_argument("-i", "--plugin-name", dest="configured_plugin_name",
        metavar="PLUGIN_NAME", help="Get information on a specific plugin name for a specific agent")

    parser_show_plugins = subparser_show.add_parser("plugins",
        help="Get information on plugins")
    parser_show_plugins.add_argument("-i", "--plugin-name", dest="available_plugin_name",
        metavar="PLUGIN_NAME", help="Get information on a specific available plugin")
    subparser_show_plugins = parser_show_plugins.add_subparsers(dest="plugin_command")
    parser_show_plugins_description = subparser_show_plugins.add_parser("description",
        help="Get information on plugin description for a specific plugin name")


    parser_authenticate = subparser_main.add_parser("authenticate",
        help="Login to CloudPoint ; Required for doing any operation")

    parser_create = subparser_main.add_parser("create",
        help="Create any information within CloudPoint")

    return parser_main

def interface(args):

    endpoint = []
    common_list = ["reports", "privileges", "roles", "email-config", "users"]

    if args.command == "show":
        if args.sub_command is None:
            print(EXIT_4)
            sys.exit(100)

        endpoint.append(GETS_DICT[args.sub_command])
        if args.sub_command in common_list:
            endpoint = decider.common_paths(endpoint, args)
        elif args.sub_command in ["assets", "agents", "plugins"]:
            endpoint = getattr(decider, args.sub_command)(endpoint, args)

        getattr(api.Command(), METHOD_DICT[args.command])('/'.join(endpoint))

    elif args.command == "authenticate":
        getattr(api.Command(), METHOD_DICT[args.command])()
        sys.exit(4)

    elif args.command == "create":
        getattr(api.Command(), METHOD_DICT[args.command])()
    else:
        print(EXIT_3)
        sys.exit(5)


def main():

    parser = create_parser()
    argcomplete.autocomplete(parser)
    args = parser.parse_args(sys.argv[1:])
    print(args)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(-1)
    else:
        interface(args)


if __name__ == "__main__":
    main()
