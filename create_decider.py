#!/usr/bin/env python3

import sys
import json
import constants as co


def common_paths(endpoint, args):

    if args.show_command == "policies":
        detail = "policy_id"
    else:
        detail = (args.show_command)[:-1] + '_id'
    if co.check_attr(args, detail):
        endpoint.append(getattr(args, detail))

    return endpoint


def roles(args):

    data = None
    if co.check_attr(args, 'file_name'):
        file_name = getattr(args, 'file_name')
        with open(file_name, 'r') as file_handle:
            try:
                data = json.load(file_handle)
            except json.decoder.JSONDecodeError:
                print("{} isn't JSON formatted, refer to the admin guide for \
formatting details.".format(file_name))
                sys.exit(-22)
    else:
        print("\nPlease choose a name that you want this role to be called")
        role_name = input("Role name : ")
        print("\nPlease choose a role type, valid role types include: ",
              ', '.join(co.VALID_PRIVILEGES))
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