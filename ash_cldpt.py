#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import sys
import reports 
import argparse
import argcomplete
import agents


def create_parser():

    parser_main = argparse.ArgumentParser()
    subparser_main = parser_main.add_subparsers(
	   dest='command', metavar='<positional argument>')

    parser_agents = subparser_main.add_parser(
        "agents", help="Agent related operations")
    subparser_agents = parser_agents.add_subparsers(
        dest="agents_command", metavar='<agent argument>')
    parser_agents_show = subparser_agents.add_parser(
        "show", help="Show agent related information")
    parser_agents_show.add_argument(
        "-i", "--agent-id", nargs='?', help="Show information related to a specific agent")
    subparser_agents_show = parser_agents_show.add_subparsers(
        dest="agents_show_command", metavar='<agent show argument>')
    parser_agents_show_plugins = subparser_agents_show.add_parser(
        "plugins", help="Show related plugins for an agent")
    parser_agents_show_plugins.add_argument(
        "plugin_id", nargs='?', help="Show plugin information for a specific agent plugin")

    parser_assets = subparser_main.add_parser(
        "assets", help="Asset releated operations")
    parser_email = subparser_main.add_parser(
        "email", help="SMTP related operations")
    parser_ldap = subparser_main.add_parser(
        "ldap", help="LDAP related operations")
    parser_licenses = subparser_main.add_parser(
        "licenses", help="Licensing related operations")
    parser_login = subparser_main.add_parser(
        "login", help="Login to perform any operations")
    parser_plugins = subparser_main.add_parser(
        "plugins", help="Plugin related operations")
    parser_policies = subparser_main.add_parser(
        "policies", help="Policy related operations")
    parser_privileges = subparser_main.add_parser(
        "privileges", help="Privilege related operations")
    parser_replication = subparser_main.add_parser(
        "replication", help="Replication related operations")
    parser_reports = subparser_main.add_parser(
        "reports", help="Report related operations")
    parser_roles = subparser_main.add_parser(
        "roles", help="Role related operations")
    parser_tags = subparser_main.add_parser(
        "tags", help="Tag related operations")
    parser_tasks = subparser_main.add_parser(
        "tasks", help="Task related operations")
    parser_telemetry = subparser_main.add_parser(
        "telemetry", help="Telemetry related operations")
    parser_users = subparser_main.add_parser(
        "users", help="User related operations")

    return parser_main

if __name__ == '__main__':

    parser_main = create_parser()
    argcomplete.autocomplete(parser_main)
    if len(sys.argv) == 1:
        parser_main.print_help()
        sys.exit(-1)
    else:
        #args = parser_main.parse_known_args(sys.argv[1:])
        args = parser_main.parse_args()
        try:
            getattr(vars()[args.command], "entry_point")()
        except KeyError:
            print("Error: '{}' module has not been implemented".format(args.command))
        except AttributeError:
            print("Error: '{}' module should have 'entry_point' function".format(args.command))
        finally:
            exit
