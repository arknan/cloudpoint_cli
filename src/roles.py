#!/usr/bin/env python3

import json
import sys
import traceback
import texttable
import api
import cloudpoint
import logs
import utils

COLUMNS = utils.get_stty_cols()
LOG_C = logs.setup(__name__, 'c')
LOG_F = logs.setup(__name__, 'f')


def entry_point(args):

    endpoint = ['/authorization/role']
    output = None
    print_args = None

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

    else:
        LOG_C.error("No arguments provided for 'roles'")
        cloudpoint.run(["roles", "-h"])
        sys.exit(1)

    return output, print_args


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
    role_type = (str(input("Role type to associate: "))).capitalize()

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
        data = json.loads(output)
        pformat = utils.print_format()

        if pformat == 'json':
            print(output)
            sys.exit(0)
        else:
            table.set_deco(pformat)

        if print_args == "role_id":
            #print(output)
            asset_list = []
            ignored = ["_links", "uri", "href", "actions", "hostId", 
                       "parentId", "snapMethods", "links"]
            required = ["name", "id", "privileges", "subjects", "autoTag", "assets"]
            table.header(["Attribute", "Value"])
            table.set_cols_dtype(['t', 't'])
            for k, v in sorted(data.items()):
                if k in required:
                    if isinstance(v, list) and v:
                        for i, _ in enumerate(v):
                            if isinstance(v[i], dict):
                                for key, value in sorted(v[i].items()):
                                    if key in required:
                                        if k == 'assets':
                                            asset_list.append(value)
                                        else:
                                            table.add_row([k.capitalize(),
                                                           value])
                    else:
                        table.add_row([k.capitalize(), v])
                if k == 'assets' and asset_list:
                    table.add_row(("Assets", ', '.join(asset_list)))

        elif print_args == 'show':
            required = ["name", "id"]
            table.header((required))

            for i, _ in enumerate(data):
                table.add_row(
                    [v for k, v in reversed(sorted(data[i].items())) if k in required])

        else:
            table.header(("Attribute", "Value"))
            table.add_rows(
                [(k, v) for k, v in sorted(data.items())],header=False)

        if table.draw():
            print(table.draw())

    except(KeyError, AttributeError, TypeError, NameError,
           texttable.ArraySizeError, json.decoder.JSONDecodeError):
        LOG_F.critical(traceback.format_exc())
        print(output)
