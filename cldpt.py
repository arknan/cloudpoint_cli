#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import sys
import argparse
import argcomplete
import api
import decider
import pdb


GETS_DICT = {
    "ad-config": "idm/config/ad",
    "agents": "agents/",
    "assets": "assets/",
    "classification-tags": "classifications/tags",
    "smtp-settings": "email/config",
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

exception_list = ["ad-config", "email setup", "report-types", "telemetry", "version", "show", "description"]

parser_main = None
sub_parser  = None



def parser_populate(parser_name, command_name, arguments={}, add_subparsers={}):

    split_var = parser_name.split('_')
    subparser_name = 'sub'
    for i in split_var[:-1]:
        subparser_name += '_' + i

    if len(command_name) == 1:
        globals()[parser_name]= globals()[subparser_name].add_parser(command_name[0], help="Get information on " + command_name[0])
    else :
        globals()[parser_name]= globals()[subparser_name].add_parser(command_name[0], help=command_name[1])

    if command_name[0] not in exception_list :
        if arguments:
            for k, v in arguments.items():
                if v is None :
                    describer = parser_name.split('_')[-2]
                    globals()[parser_name].add_argument(k, help="Get" + k + "on a" + describer)
                else :
                    if len(v) == 1:
                        my_help = "Get information on a specific "+ v[0].replace('-', '', 2)
                    else:
                        my_help = v[1]
                    metavar = v[0].replace('-', '', 2).replace('-', '_').upper()
                    globals()[parser_name].add_argument(k, v[0], metavar=metavar,
                        help=my_help)

    if add_subparsers :
        globals()['sub_'+parser_name] = globals()[parser_name].add_subparsers(dest=command_name[0] + '_command', metavar='<option>')

        for key, value in add_subparsers.items() :
            if key[0] == "Null" :
                break
            if value[0] :
                if "nested" in value:
                    parser_populate( parser_name + '_' + key[0], key, {value[0]: value[1]}, {("Null",): (None,)})
                else:
                    parser_populate( parser_name + '_' + key[0], key, {value[0]: value[1]}, {})
            else:
                parser_populate( parser_name + '_' + key[0], key, {}, {} )

def create_parser():

    global parser_main
    parser_main = \
        argparse.ArgumentParser(epilog="""\n \nFor help information\
    related to each sub-command/positional argument, \nUse "-h" or "--help"\
    at the end of that sub-command \n \nExamples : "cldpt create -h",\
    "cldpt show assets -i <ASSET_ID> --help" \n """,
                                formatter_class=argparse.RawTextHelpFormatter)
    global sub_parser
    sub_parser = parser_main.add_subparsers(dest='command', metavar='<option>')


    parser_populate("parser_show", ["show", "show operations"], {}, {("Null",): (None,)})
    parser_populate("parser_show_agents", ["agents"], {"-i": ["--agent-id"]}, {("plugins",): ("-i", ("--plugin-name",))})
    parser_populate("parser_show_plugins", ["plugins"], {"-i": ["--plugin-name"]}, {("description",): (None,)})
    parser_populate("parser_show_assets", ["assets"], {"-i": ["--asset-id"]}, {("snapshots",): ("-i", ("--snapshot-id",), "nested")})
    parser_populate("parser_show_assets_snapshots_granules", ["granules"], {"-i": ["--granule-id"]})
    parser_populate("parser_show_reports", ["reports"], {"-i": ["--report-id"]})
    parser_populate("parser_show_privileges", ["privileges"], {"-i": ["--privilege-id"]})
    parser_populate("parser_show_roles", ["roles"], {"-i": ["--role-id"]})
    parser_populate("parser_show_users", ["users"], {"-i": ["--user-id"]})
    parser_populate("parser_show_smtp-settings", ["smtp-settings", "Get information on smtp settings"])



    parser_authenticate = sub_parser.add_parser("authenticate",
        help="Login to CloudPoint ; Required for doing any operation")

    parser_create = sub_parser.add_parser("create",
        help="Create any information within CloudPoint")

    return parser_main


def interface(args, parser):

    endpoint = []
    common_list = ["reports", "privileges", "roles", "email setup", "users"]
    print(args)

    if args.command == "show":
        if args.show_command is None:
            print(EXIT_4)
            sys.exit(100)

        endpoint.append(GETS_DICT[args.show_command])
        if args.show_command in common_list:
            endpoint = decider.common_paths(endpoint, args)
        elif args.show_command in ["assets", "agents", "plugins"]:
            endpoint = getattr(decider, args.show_command)(endpoint, args)

        print(endpoint)
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
        output = interface(args, parser)
        return output

if __name__ == '__main__' :

    parser_main = create_parser()
    argcomplete.autocomplete(parser_main)
    args = parser_main.parse_args(sys.argv[1:])
    if len(sys.argv) == 1:
        parser_main.print_help()
        sys.exit(-1)
    else:
        print(interface(args, parser_main))
