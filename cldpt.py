#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import argparse
import argcomplete
import api
import sys

get_arg_mappings = {
    "ad-config" : "idm/config/ad",
    "agents" : "agents/",
    "assets" : "assets/",
    "classification-tags" : "classifications/tags",
    "granules" : "granules",
    "jointokens" : "jointokens/",
    "licenses" : "licenses/",
    "plugins" : "plugins/",
    "policies" : "policies/",
    "replication" : "replication/",
    "report-types" : "report-types/",
    "reports" : "reports/",
    "roles" : "authorization/role",
    "schedules" : "schedules/",
    "tasks" : "tasks/",
    "telemetry" : "telemetry/",
    "users" : "idm/user/",
    "version" : "version"
}

def main() :


    parser = argparse.ArgumentParser(description='CloudPoint CLI help')
    subparser = parser.add_subparsers(dest="command")

    parser_show = subparser.add_parser("show", help="show help")
    parser_show.add_argument("show_subc", help="Get information on some attribute.\
    Allowed values are => {" +", ".join(sorted(get_arg_mappings.keys())) +"}",\
    metavar='<option>', choices=sorted(get_arg_mappings.keys()))
    parser_show.add_argument("-i", "--id", \
    help="Get information on some attribute with specific ID")

    parser_auth = subparser.add_parser("authenticate", \
    help="Login to CloudPoint ; Required for doing any other operation")

    parser_create = subparser.add_parser("create", \
    help="Create any information within CloudPoint")

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if len(sys.argv) == 1 : 
        parser.print_help()
        sys.exit(1)
    else :
        interface(args)

def interface(args) :
    x = api.Command()
    if args.command  == "show":
        if args.id :
            x.gets(get_arg_mappings[args.show_subc] + '/' + args.id)
        else :
            x.gets(get_arg_mappings[args.show_subc])
    elif  args.command == "create" :
        x.posts()
    elif  args.command == "authenticate" :
        x.authenticate()

if __name__ == "__main__" :
    main()
