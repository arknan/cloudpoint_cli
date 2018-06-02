#!/usr/bin/env python3


import argparse
import api

def main() :
    get_choices = sorted(["agents", "plugins", "assets", "schedules", "policies",\
        "replication", "granules", "classification-tags", "tasks", "jointokens",\
        "telemetry", "roles", "version", "licenses",\
        "reports", "report-types" ])
    parser = argparse.ArgumentParser(description='CloudPoint CLI help')

#By default action="store" and type="string"
    parser.add_argument("-g", "--get",help="Get information on some attribute.\
    Allowed values are: {" +", ".join(get_choices) +"}", choices=get_choices, metavar='<option>')
    parser.add_argument("-a", "--authenticate", action="store_true",\
        help="Login to CloudPoint ; Required for doing any other operation")
    parser.add_argument("-c", "--create", metavar="<option>",\
    help="Create any information within CloudPoint")

    args = parser.parse_args()
    interface(args)

def interface(args) :
    x = api.Command()
    no_slashes = ["granules", "version"]
    if args.get :
        if args.get == "classification-tags":
            endpoint = "classifications/tags"
        elif args.get in no_slashes :
            endpoint = args.get
        elif args.get == "roles" :
            endpoint = "authorization/role"
        else :
            endpoint=args.get+"/"
        x.gets(endpoint)
    elif  args.create :
        x.posts()
    elif  args.authenticate :
        x.authenticate()
    else :
        print("Invalid Option")

if __name__ == "__main__" :
    main()
