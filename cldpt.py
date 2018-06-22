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


def parser_add(parser_name, command_name, arguments=None, add_subparsers=None):

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

    # if command_name[0] not in co.EXCEPTION_LIST:
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
                               {value[0]: value[1]}, None)
            else:
                parser_add(parser_name + '_' + key[0], key, None, None)


def create_parser():

    global parser_main
    parser_main = argparse.ArgumentParser(
        epilog="""
        \n \nFor help information related to each sub-command/positional\
 argument, \nUse "-h" or "--help" at the end of that sub-command \n \n
Examples : "cldpt create -h", \
"cldpt show assets -i <ASSET_ID> --help" \n """,
        formatter_class=argparse.RawTextHelpFormatter)

    global sub_parser
    sub_parser = parser_main.add_subparsers(dest='command', metavar='<option>')

    parser_add(
        "parser_show", ["show", "show operations"], None, {("Null",): (None,)})
    parser_add(
        "parser_show_agents", ["agents"], {"-i": ["--agent-id"]},
        {("plugins",): ("-i", ("--plugin-name",)),
         ("summary", "Show summary information for agents"): (None,)})
    parser_add(
        "parser_show_assets", ["assets"], {"-i": ["--asset-id"]},
        {("snapshots",): ("-i", ("--snapshot-id",), "nested"),
         ("policies",): (None,), ("summary", ): (None,)})
    parser_add(
        "parser_show_assets_snapshots_granules", ["granules"],
        {"-i": ["--granule-id"]})
    parser_add(
        "parser_show_assets_snapshots_restore-targets", ["restore-targets"])
    # parser_add("parser_show_join-tokens", ["join-tokens",
    # "Show current join-tokens"])
    parser_add(
        "parser_show_licenses", ["licenses", "Get licensing information"],
        {"-i": ["--license-id"]},
        {("active", "Get information on active licenses"): (None, ),
         ("features", "Get information on all licensed features"):
         (None, )})
    parser_add(
        "parser_show_plugins", ["plugins"], {"-i": ["--plugin-name"]},
        {("description",): (None,),
         ("summary", "Show summary information for plugins"): (None,)})
    parser_add("parser_show_policies", ["policies"], {"-i": ["--policy-id"]})
    parser_add(
        "parser_show_privileges", ["privileges"], {"-i": ["--privilege-id"]})
    parser_add(
        "parser_show_replication", ["replication", "Get replication policies"],
        {"-i": ["--policy-name"]}, {(
            "rules", "Show replication rules for a policy"): (None, )})
    parser_add(
        "parser_show_reports", ["reports"], {"-i": ["--report-id"]},
        {("report-data", "Show data collected by a specific report"):
         (None,), ("preview", "Show first 10 lines of the report data"):
         (None,)})
    parser_add("parser_show_roles", ["roles"], {"-i": ["--role-id"]})
    parser_add(
        "parser_show_settings", ["settings"], None,
        {("ad", "Get information on Active-Directory/LDAP settings"):
         (None,), ("smtp", "Get information on smtp settings"): (None,)})
    parser_add("parser_show_tags", ["tags", "Get classification tags"])
    parser_add(
        "parser_show_tasks", ["tasks"], {
            "-i": ["--task-id"], "-s": [
                "--status", "Filter on status, valid values for status are :\
                ['running', 'successful', 'failed']"],
            "-r": [
                "--run-since",
                "Filter on tasks started in last <RUN_SINCE> no. of hours"],
            "-t": [
                "--taskType", "Filter on task type, valid values for \
                task types are : ['create-snapshot', 'create-group-snapshot',\
                'delete-snapshot', 'delete-group-snapshots', 'restore',\
                'delete-snapshot']"],
            "-l": ["--limit", "Limit number of results"]},
        {("summary", "Get summary information of snapshot tasks"): (None,)})
    parser_add("parser_show_users", ["users"], {"-i": ["--user-id"]})
    parser_add(
        "parser_show_telemetry",
        ["telemetry", "Get information on Telemetry status"])
    parser_add(
        "parser_show_version",
        ["version", "Get current CloudPoint version"])

    parser_add(
        "parser_authenticate", [
            "authenticate",
            "Login to CloudPoint ; Required for doing any operation"])

    parser_add(
        "parser_create", [
            "create", "Create any information within CloudPoint"], None,
        {("Null",): (None,)})
    parser_add("parser_create_role-assignments", [
        "role-assignments", "Assign an existing role to an existing user"])
    parser_add("parser_create_email-config", [
        "email_config", "Integrate SMTP"])
    parser_add("parser_create_user", [
        "user", "Create a new user within CloudPoint"])
    parser_add("parser_create_snapshots", [
        "snapshots", "Take snapshots of assets"],
        {"-i": ["--asset-id", "Provide an ASSET_ID to snap"]})
    parser_add("parser_create_replicas", [
        "replicas", "Replicate existing snapshots"],
        {"-i": ["--snap-id", "Provide a SNAPSHOT_ID to replicate"]})
    parser_add("parser_create_policies", ["policies", "Create Policies"])
    # parser_add("parser_create_privilege")
    # ("-f", ("--file-name", "JSON formatted file with role details"))})

    parser_add(
        "parser_modify", [
            "modify", "Modify any information within CloudPoint"], None,
        {("Null",): (None,)})
    parser_add("parser_modify_reset-password", [
        "reset_password", "Reset a user's password"])

    parser_add(
        "parser_restore", ["restore", "Restore snapshots"],
        {"-i": ["--snap-id", "Provide a SNAPSHOT_ID to restore"]})

    return parser_main


def interface(arguments):

    endpoint = []

    if arguments.command == "show":
        if arguments.show_command is None:
            globals()['parser_show'].print_help()
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

    elif arguments.command == "authenticate":
        getattr(api.Command(), co.METHOD_DICT[arguments.command])()
        sys.exit(4)

    elif arguments.command == "create":
        if arguments.create_command is None:
            globals()['parser_create'].print_help()
            sys.exit(100)
        # elif arguments.create_command == "role_assignments":
        #    endpoint.append('/authorization/role')
        elif arguments.create_command in co.POST_DICT:
            endpoint.append(co.POST_DICT[arguments.create_command])
        elif arguments.create_command in ["snapshots", "replicas"]:
            pass
        else:
            print("That is not a valid endpoint to fetch\n")

        data, endpoint = getattr(
            create_decider, arguments.create_command)(arguments, endpoint)

        if arguments.create_command in co.PUTS_LIST:
            return (getattr(api.Command(), "puts")(
                '/'.join(endpoint), data), endpoint)

        return (getattr(api.Command(), co.METHOD_DICT[arguments.command])(
            '/'.join(endpoint), data), endpoint)

    elif arguments.command == "modify":
        if arguments.modify_command is None:
            globals()['parser_modify'].print_help()
            sys.exit(100)
        elif arguments.modify_command in co.POST_DICT:
            endpoint.append(co.POST_DICT[arguments.modify_command])
        else:
            print("That is not a valid endpoint to fetch\n")

        data = getattr(modify_decider, arguments.modify_command)()

        if arguments.modify_command in co.PUTS_LIST:
            return (getattr(api.Command(), "puts")(
                '/'.join(endpoint), data), endpoint)
    
    elif arguments.command == "restore":
        endpoint.append(co.GETS_DICT["assets"])
        data, endpoint = getattr(create_decider, "restore")(
            arguments, endpoint)
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
