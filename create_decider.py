#!/usr/bin/env python3

import sys
import json
import cldpt
import constants as co


def role_assignments():

    """
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
    """

    print("\nPlease choose a name that you want this role to be called")
    role_name = input("Role name : ")
    roles = json.loads(cldpt.run(["show", "privileges"]))
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
