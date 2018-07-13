#!/usr/bin/env python3

import sys
import json
import api
import constants as co

def entry_point(args):

    endpoint = []
    if args.replication_command == "show":
        endpoint.append(co.GETS_DICT[args.command])
        show(args, endpoint)
        output = getattr(api.Command(), co.METHOD_DICT[args.replication_command])('/'.join(endpoint))
    elif  args.replication_command == "create":
        if not co.check_attr(args, 'replication_create_command'):
            print("Invalid argument : '{}'".format(args.replication_create_command))
            sys.exit(-1)

        endpoint.append(co.POSTS_DICT[args.replication_create_command])
        data = create(args, endpoint)
        output = getattr(api.Command(), co.METHOD_DICT['create'])('/'.join(endpoint), data)

    else:
        print("Invalid '{}' argument : '{}'".format(__name__, args.replication_command))
        sys.exit(-1)

    return output

def show(args, endpoint):

    if co.check_attr(args, 'policy_name'):
        endpoint.append(getattr(args, 'policy_name'))

    if co.check_attr(args, 'replication_show_command'):
        if co.check_attr(args, 'policy_name'):
            endpoint.append('/rules/')
        else:
            endpoint.append('/default/rules/')

def create(args, endpoint):

    repl_locations = json.loads(getattr(api.Command(), 'gets')(
        '/replica-locations/'))
    valid_sources = {x['region']: x['id'] for x in repl_locations}
    source = None
    while True:
        print("Enter a source region, valid values are:\n{}".format(
            list(valid_sources.keys())))
        source_region = input("Source region : ")
        if source_region in valid_sources:
            source = (valid_sources[source_region])
            del valid_sources[source_region]
            break
        else:
            print("Not a valid choice, please try again\n")

    dest_counter = 0
    dest = []
    while dest_counter < 3:
        print("Valid destination regions are : {}".format(
            list(valid_sources.keys())))
        temp = input("Destination : (enter 'none' if you are done) ")
        if temp == 'none':
            break

        elif temp in valid_sources:
            dest.append(valid_sources[temp])
            dest_counter += 1

        else:
            print("\nNot a valid location\n")

    if not dest:
        print("\nYou should provide atleast 1 region to replicate to !\n")
        sys.exit(-1)

    data = {
        "destination": dest,
        "source": source
    }

    return data

def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format that makes parsing easier !
    print(data)
