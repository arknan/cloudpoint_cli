#!/usr/bin/env python3


import argparse
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
    subparser = parser.add_subparsers(dest="sc", help="Sub-Command Help")

    parser_show = subparser.add_parser("show", help="show help")
    parser_show.add_argument("sc_value", help="Get information on some attribute.\
    Allowed values are: {" +", ".join(sorted(get_arg_mappings.keys())) +"}",\
    metavar='<option>')
    parser_show.add_argument("-i", "--id", \
    help="Get information on some attribute with specific ID")

    parser_auth = subparser.add_parser("authenticate", \
    help="Login to CloudPoint ; Required for doing any other operation")

    parser_create = subparser.add_parser("create", \
    help="Create any information within CloudPoint")

    args = parser.parse_args()
    print(args)
    if len(sys.argv) == 1 : 
        parser.print_help()
        sys.exit(1)
    else :
        interface(args)

def interface(args) :
    x = api.Command()
    if args.sc :
        if args.id :
            x.gets(get_arg_mappings[args.sc_value] + '/' + args.id)
        else :
            x.gets(get_arg_mappings[args.sc_value])
    elif  args.create :
        x.posts()
    elif  args.authenticate :
        x.authenticate()

if __name__ == "__main__" :
    main()
