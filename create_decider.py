#!/usr/bin/env python3

import sys
import json
from getpass import getpass
import constants as co
import cldpt


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


def email_config():

    # This doesn't seem to work currently,
    # maybe the data format is wrong ! need to check with ENGG
    print("\nPlease enter the IP address of SMTP server")
    smtp_ip = input("IP Address : ")
    print("\nPlease enter the port used by SMTP")
    smtp_port = input("Port (25) : ")
    if not smtp_port:
        smtp_port = 25
    print("\nPlease enter SMTP credentials [skip if anonymous authentication]")
    smtp_user = input("User name : ")
    smtp_passwd = None
    auth = False
    if smtp_user:
        auth = True
        smtp_passwd = getpass("Password: ")
    print("\nPlease enter the smtp sender email address")
    smtp_email = input("Sender Email : ")

    data = {
        "type": "smtp",
        "senderEmail": smtp_email,
        "data": {
            "host": smtp_ip,
            "port": smtp_port,
            "authentication": "false"
        }
    }
    if auth:
        data["data"]["username"] = smtp_user
        data["data"]["password"] = smtp_passwd
        data["data"]["authentication"] = "true"

    return data


def user():

    print("\nPlease note that users must be accessible by both ", end='')
    print("LDAP[Name] and SMTP[email address]")
    first_name = input("Firstname : ")
    last_name = input("Lastname : ")
    email_addr = input("Email : ")

    data = {
        "lastName": last_name,
        "email": email_addr,
        "firstName": first_name
    }

    return data
