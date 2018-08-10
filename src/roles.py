#!/usr/bin/env python3

import json
import sys
import api
import cloudpoint
import constants as co
import logs

logger_c = logs.setup(__name__, 'c')


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
        show(args, endpoint)
        output = getattr(api.Command(), 'gets')('/'.join(endpoint))

    else:
        logger_c.error("No arguments provided for 'roles'\n")
        cloudpoint.run(["roles", "-h"])
        sys.exit()

    return output


def create():

    VALID_PRIVILEGES = ["REPLICATION_POLICY_MANAGEMENT", "REPORT_MANAGEMENT",
                    "SNAPSHOT_POLICY_MANAGEMENT", "ROLE_MANAGEMENT",
                    "CLASSIFICATION_POLICY_MANAGEMENT", "USER_MANAGEMENT",
                    "CLOUD_AND_ARRAY_MANAGEMENT", "ADMINISTRATOR"]

    role_name = input("Role name : ")
    roles = json.loads(cloudpoint.run(["privileges", "show"]))
    roles_list = []
    for row in roles:
        roles_list.append(row["name"])
    logger_c.info("Please choose a role type, valid role types include : ",
          roles_list)
    role_type = (str(input("Role type to associate: "))).upper()

    if role_type not in co.VALID_PRIVILEGES:
        logger_c.error("That is not a valid role type !")
        sys.exit()

    logger_c.info("Enter the user's email address that should be associated \
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

    if co.check_attr(args, 'role_id'):
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
        logger_c.error("Role '{}' doesn't exist".format(data["name"]))
        sys.exit()
    else:
        endpoint.append(role_id)

    return data


def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format
    print(data)


def show(args, endpoint):
    if co.check_attr(args, 'role_id'):
        endpoint.append(args.role_id)
