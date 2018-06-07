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
    "email setup": "email/config",
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
    subparser_main = parser_main.add_subparsers(dest='command', metavar='<option>')

    parser_show = subparser_main.add_parser("show", help="show operations") 
    subparser_show = parser_show.add_subparsers(dest="sub_command", metavar='<option>', help="Please provide any one of the following options : ") 

    exception_list = ["ad-config", "email setup", "description", "report-types", "telemetry", "version"]

    def create_args(sub_parser_name, parser_name, command_name):
        globals()[parser_name]= sub_parser_name.add_parser(command_name, help="Get information on "+command_name) 
        if command_name not in exception_list :
            globals()[parser_name].add_argument("-i", '--'+command_name[:-1]+'-id',
                help="Get information on a specific "+ command_name[:-1]+' ID')

    create_args(subparser_show, "parser_show_assets", "assets")
    subparser_show_assets = parser_show_assets.add_subparsers(dest="asset_command", metavar='<option>')
    create_args(subparser_show_assets, "parser_show_assets_snapshots", "snapshots")
    subparser_show_assets_snapshots =\
        parser_show_assets_snapshots.add_subparsers(dest="snapshot_command", metavar='<option>')
    create_args(subparser_show_assets_snapshots, "parser_show_assets_snapshots_granules", "granules")

    create_args(subparser_show, "parser_show_agents", "agents")
    subparser_show_agents = parser_show_agents.add_subparsers(dest="agent_command", metavar='<option>')
    parser_show_agents_plugins = subparser_show_agents.add_parser("plugins",
        help="Get information on plugins for a specific agent")
    parser_show_agents_plugins.add_argument("-i", "--plugin-name", dest="configured_plugin_name",
        metavar="PLUGIN_NAME", help="Get information on a specific plugin name for a specific agent")

    create_args(subparser_show, "parser_show_plugins", "plugins")
    subparser_show_plugins = parser_show_plugins.add_subparsers(dest="plugin_command", metavar='<option>')
    create_args(subparser_show_plugins, "parser_show_plugins_description", "description")

    show_parser_dict = {
    "parser_show_reports": "reports",
    "parser_show_privileges": "privileges",
    "parser_show_roles": "roles",
    "parser_show_users": "users",
    "parser_show_email setup": "email setup"
    }

    for k,v in sorted(show_parser_dict.items()):
        create_args(subparser_show, k, v)


    parser_authenticate = subparser_main.add_parser("authenticate",
        help="Login to CloudPoint ; Required for doing any operation")

    parser_create = subparser_main.add_parser("create",
        help="Create any information within CloudPoint")

    return parser_main

def interface(args):

    endpoint = []
    common_list = ["reports", "privileges", "roles", "email setup", "users"]

    if args.command == "show":
        if args.sub_command is None:
            print(EXIT_4)
            sys.exit(100)

        endpoint.append(GETS_DICT[args.sub_command])
        if args.sub_command in common_list:
            endpoint = decider.common_paths(endpoint, args)
        elif args.sub_command in ["assets", "agents", "plugins"]:
            endpoint = getattr(decider, args.sub_command)(endpoint, args)

        output = getattr(api.Command(), METHOD_DICT[args.command])('/'.join(endpoint))
        return output

    elif args.command == "authenticate":
        getattr(api.Command(), METHOD_DICT[args.command])()
        sys.exit(4)

    elif args.command == "create":
        getattr(api.Command(), METHOD_DICT[args.command])()
    else:
        print(EXIT_3)
        sys.exit(5)


def run(pass_args=None):

    parser = create_parser()
    argcomplete.autocomplete(parser)
    args = parser.parse_args(pass_args)
    if len(pass_args) == 1:
        parser.print_help()
    else:
        output = interface(args)
        return output


if __name__ == "__main__":
    parser = create_parser()
    argcomplete.autocomplete(parser)
    args = parser.parse_args(sys.argv[1:])
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(-1)
    else:
        print(interface(args))
