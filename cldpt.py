#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import sys
import argparse
import argcomplete
import api
import decider
import constants as co


def parser_add(parser_name, command_name, arguments={}, add_subparsers={}):

    split_var = parser_name.split('_')
    subparser_name = 'sub'
    for i in split_var[:-1]:
        subparser_name += '_' + i

    if len(command_name) == 1:
        globals()[parser_name] = globals()[subparser_name].add_parser(
            command_name[0], help="Get information on " + command_name[0])
    else:
        globals()[parser_name] = globals()[subparser_name].add_parser(
            command_name[0], help=command_name[1])

    if command_name[0] not in co.EXCEPTION_LIST:
        if arguments:
            for key, value in sorted(arguments.items()):
                if value is None:
                    # describer = parser_name.split('_')[-2]
                    globals()[parser_name].add_argument(key)
                else:
                    if len(value) == 1:
                        describer = value[0].replace('-', '', 2)
                        describer = describer.replace('-', '_').upper()
                        my_help = "Get information on a specific " + describer
                    else:
                        my_help = value[1]
                    metavalue = value[0].replace('-', '', 2)
                    metavalue = metavalue.replace('-', '_').upper()
                    globals()[parser_name].add_argument(
                        key, value[0], metavar=metavalue, help=my_help)

    if add_subparsers:
        globals()['sub_'+parser_name] = globals()[parser_name].add_subparsers(
            dest=command_name[0] + '_command', metavar='<option>')

        for key, value in sorted(add_subparsers.items()):
            if key[0] == "Null":
                break
            if value[0]:
                if "nested" in value:
                    parser_add(parser_name + '_' + key[0], key,
                               {value[0]: value[1]}, {("Null",): (None,)})
                else:
                    parser_add(parser_name + '_' + key[0], key,
                               {value[0]: value[1]}, {})
            else:
                parser_add(parser_name + '_' + key[0], key, {}, {})


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

    parser_add("parser_show", ["show", "show operations"], {},
               {("Null",): (None,)})
    parser_add("parser_show_agents", ["agents"], {"-i": ["--agent-id"]},
               {("plugins",): ("-i", ("--plugin-name",)), ("summary",
               "Show summary information for agents"): (None,)})
    parser_add("parser_show_assets", ["assets"], {"-i": ["--asset-id"]},
               {("snapshots",): ("-i", ("--snapshot-id",), "nested"),
                ("policies",): (None,), ("summary", ): (None,)})
    parser_add("parser_show_assets_snapshots_granules", ["granules"],
               {"-i": ["--granule-id"]})
    parser_add("parser_show_licenses", ["licenses",
               "Get licensing information"], {"-i": ["--license-id"]}, {(
               "active", "Get information on active licenses"): (None, ), (
               "features", "Get information on all licensed features"): (
               None, )})
    parser_add("parser_show_plugins", ["plugins"], {"-i": ["--plugin-name"]},
               {("description",): (None,), ("summary", "Show summary\
               information for plugins"): (None,)})
    parser_add("parser_show_policies", ["policies"],
               {"-i": ["--policy-id"]})
    parser_add("parser_show_privileges", ["privileges"],
               {"-i": ["--privilege-id"]})
    parser_add("parser_show_replication", ["replication",
               "Get replication rules"])
    parser_add("parser_show_reports", ["reports"], {"-i": ["--report-id"]}, {
               ("report-data", "Show data collected by a specific report"): (
               None,), ("preview", "Show first 10 lines of the report data"): (
               None,)})
    parser_add("parser_show_roles", ["roles"], {"-i": ["--role-id"]})
    parser_add("parser_show_settings", ["settings"], {}, {("ad",
               "Get information on Active-Directory/LDAP settings"): (None,), (
               "smtp", "Get information on smtp settings"): (None,)})
    parser_add("parser_show_tasks", ["tasks"], {"-i": ["--task-id"], "-s": [
               "--status", "Filter on status, valid values for status are :\
               ['running', 'successful', 'failed']"], "-r": ["--run-since",
               "Filter on tasks started in the last <RUN_SINCE> no. of hours"],
               "-t": ["--taskType", "Filter on task type, valid values for \
               task types are : ['create-snapshot', 'create-group-snapshot',\
               'delete-snapshot', 'delete-group-snapshots', 'delete-snapshot',\
               'restore']"], "-l": ["--limit", "Limit number of results"]},
               {("summary", "Get summary information of snapshot tasks"): (
               None,)})
    parser_add("parser_show_users", ["users"], {"-i": ["--user-id"]})
    parser_add("parser_show_telemetry", ["telemetry",
               "Get information on Telemetry status"])
    parser_add("parser_show_version", ["version",
               "Get current CloudPoint version"])

    parser_add("parser_login", ["login",
               "Login to CloudPoint ; Required for doing any operation"])
    parser_add("parser_create",
               ["create", "Create any information within CloudPoint"])

    return parser_main


def interface(arguments):

    endpoint = []

    if arguments.command == "show":
        if arguments.show_command is None:
            globals()['parser_show'].print_help()
            sys.exit(100)

        endpoint.append(co.GETS_DICT[arguments.show_command])
        if arguments.show_command in co.COMMON_DECIDER_PATHS:
            endpoint = decider.common_paths(endpoint, arguments)
        elif arguments.show_command in co.DECIDER_PATHS:
            endpoint = getattr(decider,
                               arguments.show_command)(endpoint, arguments)

        # print(endpoint)
        response = getattr(api.Command(),
                         co.METHOD_DICT[arguments.command])('/'.join(endpoint))
        return (response, endpoint)

    elif arguments.command == "login":
        getattr(api.Command(), co.METHOD_DICT[arguments.command])()
        sys.exit(4)

    elif arguments.command == "create":
        getattr(api.Command(), co.METHOD_DICT[arguments.command])()
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
        output, endpoint = interface(args)
        print(output)
