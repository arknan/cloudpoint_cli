#!/usr/bin/env python3

import sys
import json
import api
import cldpt
import constants as co


def entry_point(args):

    endpoint = []

    if args.roles_command == "show":
        endpoint.append(co.GETS_DICT[args.command])
        show(args, endpoint)
        output = getattr(
            api.Command(), co.METHOD_DICT['show'])('/'.join(endpoint))

    elif args.roles_command == "create":
        endpoint.append(co.POSTS_DICT[args.roles_create_command])
        data = create()
        output = getattr(
            api.Command(), co.METHOD_DICT['create'])('/'.join(endpoint), data)

    elif args.roles_command == "delete":
        endpoint.append(co.GETS_DICT[args.command])
        delete(args, endpoint)
        output = getattr(
            api.Command(), co.METHOD_DICT['delete'])('/'.join(endpoint))

    else:
        print("No arguments provided for 'roles'\n")
        cldpt.run(["roles", "-h"])
        sys.exit(-1)

    return output


def show(args, endpoint):
    if co.check_attr(args, 'role_id'):
        endpoint.append(args.role_id)


def create():

    print("\nPlease choose a name that you want this role to be called")
    role_name = input("Role name : ")
    roles = json.loads(cldpt.run(["privileges", "show"]))
    roles_list = []
    for row in roles:
        roles_list.append(row["name"])
    print("\nPlease choose a role type, valid role types include : ",
          roles_list)
    role_type = str(input("Role type to associate: "))
    if role_type not in co.VALID_PRIVILEGES:
        print("\nThat is not a valid role type !\n")
        sys.exit(-23)
    print("\nEnter the user's email address that should be associated \
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


def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format
    print(data)
