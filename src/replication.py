#!/usr/bin/env python3

import json
import sys
import texttable
import api
import cloudpoint
import logs

LOG_C = logs.setup(__name__, 'c')


def entry_point(args):

    endpoint = []

    if args.replication_command == "create":
        endpoint.append('/replication/default/rules/')
        data = create(args)
        output = getattr(api.Command(), 'posts')('/'.join(endpoint), data)

    elif args.replication_command == "delete":
        if not api.check_attr(args, 'replication_delete_command'):
            LOG_C.error("No arguments provided for 'delete'")
            cloudpoint.run(["replication", "delete", "-h"])
            sys.exit(1)

        endpoint.append('/replication/default/rules/')
        delete(endpoint)
        output = getattr(api.Command(), 'deletes')('/'.join(endpoint))

    elif args.replication_command == "modify":
        if not api.check_attr(args, 'replication_modify_command'):
            LOG_C.error("No arguments provided for 'modify'")
            cloudpoint.run(["replication", "modify", "-h"])
            sys.exit(1)

        endpoint.append('/replication/default/rules/')
        data = modify(args, endpoint)
        output = getattr(api.Command(), 'puts')('/'.join(endpoint), data)

    elif args.replication_command == "show":
        endpoint.append('/replication/')
        show(args, endpoint)
        output = getattr(
            api.Command(), 'gets')('/'.join(endpoint))

    else:
        LOG_C.error("No arguments provided for 'replication'")
        cloudpoint.run(["replication", "-h"])
        sys.exit(1)

    return output


def create(args):

    if not api.check_attr(args, 'replication_create_command'):
        LOG_C.error("No arguments provided for 'create'")
        cloudpoint.run(["replication", "create", "-h"])
        sys.exit(1)

    repl_locations = json.loads(getattr(api.Command(), 'gets')(
        '/replica-locations/'))
    valid_sources = {x['region']: x['id'] for x in repl_locations}
    source = None
    while True:
        LOG_C.info("Enter a source region, valid values are:\n%s",
                   list(valid_sources.keys()))
        source_region = input("Source region : ")
        if source_region in valid_sources:
            source = (valid_sources[source_region])
            del valid_sources[source_region]
            break
        else:
            LOG_C.error("Not a valid choice, please try again")

    dest_counter = 0
    dest = []
    while dest_counter < 3:
        LOG_C.info("Valid destination regions are : %s",
                   list(valid_sources.keys()))
        temp = input("Destination : (enter 'none' if you are done) ")
        if temp == 'none':
            break

        elif temp in valid_sources:
            dest.append(valid_sources[temp])
            dest_counter += 1

        else:
            LOG_C.error("Not a valid location")

    if not dest:
        LOG_C.error("You should provide atleast 1 region to replicate to !")
        sys.exit(1)

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
    LOG_C.info(
        "Enter the source region of the replication rule to be deleted\n")
    while True:
        LOG_C.info("Valid source regions :%s\n",
                   sorted(valid_sources.keys()))
        src_region = input("Source Region : ")
        if src_region in valid_sources:
            break
        else:
            LOG_C.error(
                "No replication rule exists for this source region\n")
            LOG_C.error("Enter a valid source region to delete\n")

    endpoint.append(valid_sources[src_region])


def modify(args, endpoint):

    create_data = create(args)
    endpoint.append('/' + create_data["source"])
    data = {
        "destination": create_data["destination"]
    }

    return data


def show(args, endpoint):

    if api.check_attr(args, 'policy_name'):
        endpoint.append(getattr(args, 'policy_name'))

    if api.check_attr(args, 'replication_show_command'):
        if api.check_attr(args, 'policy_name'):
            endpoint.append('/rules/')
        else:
            endpoint.append('/default/rules/')


def pretty_print(args, output):

    try:
        table = texttable.Texttable()
        data = json.loads(output)

        if args.policy_name:
            table.header([k for k, v in sorted(data.items())])
            table.add_row([v for k, v in sorted(data.items())])

        else:
            for i, _ in enumerate(data):
                table.header([k for k, v in sorted(data[i].items())])
                table.add_row([v for k, v in sorted(data[i].items())])

        if table.draw():
            print(table.draw())

    except(KeyError, AttributeError, TypeError, NameError, texttable.ArraySizeError, json.decoder.JSONDecodeError):
        print(output)
