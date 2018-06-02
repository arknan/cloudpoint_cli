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

    #By default action="store" and type="string"
    parser.add_argument("-g", "--get",help="Get information on some attribute.\
    Allowed values are: {" +", ".join(sorted(get_arg_mappings.keys())) +"}", choices=sorted(get_arg_mappings.keys()), metavar='<option>')

    parser.add_argument("-a", "--authenticate", action="store_true",\
        help="Login to CloudPoint ; Required for doing any other operation")

    parser.add_argument("-c", "--create", metavar="<option>",\
    help="Create any information within CloudPoint")

    args = parser.parse_args()
    if len(sys.argv) == 1 : 
        parser.print_help()
        sys.exit(1)
    else :
        interface(args)

def interface(args) :
    x = api.Command()
    if args.get :
        x.gets(get_arg_mappings[args.get])
    elif  args.create :
        x.posts()
    elif  args.authenticate :
        x.authenticate()

if __name__ == "__main__" :
    main()
