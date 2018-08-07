#!/usr/bin/env python3

import sys
import json
import api
import cloudpoint
import constants as co


def entry_point(args):

    endpoint = []

    if args.replication_command == "create":
        if not co.check_attr(args, 'replication_create_command'):
            print("No arguments provided for 'create'\n")
            cloudpoint.run(["replication", "create", "-h"])
            sys.exit(-1)

        endpoint.append('/replication/default/rules/')
        data = create()
        output = getattr(api.Command(), 'posts')('/'.join(endpoint), data)

    elif args.replication_command == "delete":
        if not co.check_attr(args, 'replication_delete_command'):
            print("No arguments provided for 'delete'\n")
            cloudpoint.run(["replication", "delete", "-h"])
            sys.exit(-1)

        endpoint.append('/replication/default/rules/')
        delete(endpoint)
        output = getattr(api.Command(), 'deletes')('/'.join(endpoint))

    elif args.replication_command == "modify":
        if not co.check_attr(args, 'replication_modify_command'):
            print("No arguments provided for 'modify'\n")
            cloudpoint.run(["replication", "modify", "-h"])
            sys.exit()

        endpoint.append('/replication/default/rules/')
        data = modify(endpoint)
        output = getattr(api.Command(), 'puts')('/'.join(endpoint), data)

    elif args.replication_command == "show":
        endpoint.append('/replication/')
        show(args, endpoint)
        output = getattr(
            api.Command(), 'gets')('/'.join(endpoint))

    else:
        print("No arguments provided for 'replication'\n")
        cloudpoint.run(["replication", "-h"])
        sys.exit(-1)

    return output


def create():

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


def delete(endpoint):

    repl_locations = json.loads(getattr(api.Command(), 'gets')(
        '/replica-locations/'))
    valid_sources = {x['region']: x['id'] for x in repl_locations}

    existing_locations = json.loads(cloudpoint.run(
        ["replication", "show", "rules"]))
    existing_sources = [existing_locations[x]['source'] for x, _ in enumerate(
        existing_locations)]

    for k in list(sorted(valid_sources)):
        if not valid_sources[k] in existing_sources:
            del valid_sources[k]

    src_region = None
    print("Enter the source region of the replication rule to be deleted\n")
    while True:
        print("Valid source regions :\n", sorted(valid_sources.keys()))
        src_region = input("Source Region : ")
        if src_region in valid_sources:
            break
        else:
            print("No replication rule exists for the source region\n")
            print("Enter a valid source region to delete\n")
    endpoint.append(valid_sources[src_region])


def modify(endpoint):

    create_data = create()
    endpoint.append('/' + create_data["source"])
    data = {
        "destination": create_data["destination"]
    }

    return data


def show(args, endpoint):

    if co.check_attr(args, 'policy_name'):
        endpoint.append(getattr(args, 'policy_name'))

    if co.check_attr(args, 'replication_show_command'):
        if co.check_attr(args, 'policy_name'):
            endpoint.append('/rules/')
        else:
            endpoint.append('/default/rules/')


def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format
    print(data)
