#!/usr/bin/env python3

import sys
import json
import api
import ash_cldpt
import constants as co

def entry_point(args):

    endpoint = []

    if args.roles_command == "show":
        endpoint.append(co.GETS_DICT[args.command])
        if co.check_attr(args, 'roles_command'):
            globals()[args.roles_command](args, endpoint)
        else:
            print("Invalid argument : '{}'".format(args.roles_command))
            sys.exit(-1)
        output = getattr(api.Command(), co.METHOD_DICT['show'])('/'.join(endpoint))

    elif args.roles_command == "create":
        data = None
        endpoint.append(co.POSTS_DICT[args.roles_create_command])
        if co.check_attr(args, 'roles_command'):
            data = globals()[args.roles_command](args, endpoint)
        else:
            print("Invalid argument : '{}'".format(args.roles_command))
            sys.exit(-1)
        output = getattr(api.Command(), co.METHOD_DICT['create'])('/'.join(endpoint), data)

    return output

def show(args, endpoint):
    if co.check_attr(args, 'role_id'):
        endpoint.append(args.role_id)

    return endpoint

def create(args, endpoint):

    print("\nPlease choose a name that you want this role to be called")
    role_name = input("Role name : ")
    roles = json.loads(ash_cldpt.run(["privileges", "show"]))
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

def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format that makes parsing easier !
    print(data)
