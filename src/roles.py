#!/usr/bin/env python3

import json
import sys
import texttable
import api
import cloudpoint
import logs
import utils

COLUMNS = utils.get_stty_cols()
LOG_C = logs.setup(__name__, 'c')


def entry_point(args):

    endpoint = ['/authorization/role']

    if args.roles_command == "create":
        data = create()
        output = getattr(api.Command(), 'posts')('/'.join(endpoint), data)

    elif args.roles_command == "delete":
        delete(args, endpoint)
        output = getattr(api.Command(), 'deletes')('/'.join(endpoint))

    elif args.roles_command == "modify":
        data = modify(endpoint)
        output = getattr(api.Command(), 'puts')('/'.join(endpoint), data)

    elif args.roles_command == "show":
        print_args = show(args, endpoint)
        output = getattr(api.Command(), 'gets')('/'.join(endpoint))
        pretty_print(output, print_args)

    else:
        LOG_C.error("No arguments provided for 'roles'")
        cloudpoint.run(["roles", "-h"])
        sys.exit(1)

    return output


def create():

    valid_privileges = ["REPLICATION_POLICY_MANAGEMENT", "REPORT_MANAGEMENT",
                        "SNAPSHOT_POLICY_MANAGEMENT", "ROLE_MANAGEMENT",
                        "CLASSIFICATION_POLICY_MANAGEMENT", "USER_MANAGEMENT",
                        "CLOUD_AND_ARRAY_MANAGEMENT", "ADMINISTRATOR"]

    role_name = input("Role name : ")
    roles = json.loads(cloudpoint.run(["privileges", "show"]))
    roles_list = []
    for row in roles:
        roles_list.append(row["name"])
    LOG_C.info(
        "Please choose a role type. Valid role types include:\n%s", roles_list)
    role_type = (str(input("Role type to associate: "))).upper()

    if role_type not in valid_privileges:
        LOG_C.error("That is not a valid role type !")
        sys.exit(1)

    LOG_C.info("Enter the user's email address that should be associated \
with this role")
    user_email = str(input("Email Address : "))

    data = {
        "name": role_name,
        "privileges": [{
            "name": role_type
        }],
        "subjects": [{
            "name": user_email
        }]
    }

    return data


def delete(args, endpoint):

    if utils.check_attr(args, 'role_id'):
        endpoint.append('/' + args.role_id)
    else:
        role_id = input("Enter role id of the role you want to delete : ")
        endpoint.append('/' + role_id)


def modify(endpoint):
    data = create()
    roles_dict = json.loads(cloudpoint.run(["roles", "show"]))
    role_id = None

    for num, _ in enumerate(roles_dict):
        if data["name"] == roles_dict[num]['name']:
            role_id = roles_dict[num]['id']

    if not role_id:
        LOG_C.error("Role '%s' doesn't exist", data["name"])
        sys.exit(1)
    else:
        endpoint.append(role_id)

    return data


def show(args, endpoint):

    print_args = None
    if utils.check_attr(args, 'role_id'):
        endpoint.append(args.role_id)
        print_args = "role_id"
    else:
        print_args = "show"

    return print_args


def pretty_print(output, print_args):

    try:
        table = texttable.Texttable(max_width=COLUMNS)
        table.set_deco(texttable.Texttable.HEADER)
        data = json.loads(output)

        if print_args == "role_id":
            ignored = ["links", "uri"]
            for k, v in sorted(data.items()):
                if isinstance(v, list) and v:
                    for i, _ in enumerate(v):
                        if isinstance(v[i], dict):
                            for key, value in sorted(v[i].items()):
                                if key not in ignored and k not in ignored:
                                    table.add_row([k, (key, value)])
                        else:
                            table.add_row([k, v])

                else:
                    table.add_row([k, v])
        else:
            required = ["id", "name"]

            for i, _ in enumerate(data):
                table.header(sorted(required))
                table.add_row(
                    [v for k, v in sorted(data[i].items()) if k in required])

        if table.draw():
            print(table.draw())

    except(KeyError, AttributeError, TypeError, NameError, texttable.ArraySizeError, json.decoder.JSONDecodeError):
        print(output)
