#!/usr/bin/env python3

import sys
import json
from re import findall
from getpass import getpass
import constants as co
import cldpt


def role_assignments(args, endpoint):

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

    return (data, endpoint)


def email_config(args, endpoint):

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
    rint("\nPlease enter the smtp sender email address")
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

    return (data, endpoint)


def user(args, endpoint):

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

    return (data, endpoint)

def snapshots(args, endpoint):

    if co.check_attr(args, "asset_id"):
       endpoint.append('/assets/')
       endpoint.append(args.asset_id)
       endpoint.append('/snapshots/')
    else:
        print("\nPlease mention an ASSET_ID for taking snapshot\n")
        sys.exit(-1)

    snap_types = json.loads(cldpt.run(["show", "assets", "-i", args.asset_id]))["snapMethods"]
    print("\nPlease enter a snapshot type")
    print("Valid types for this asset include :", snap_types)
    snap_type = input("SnapType : ")
    snap_name = input("Snapshot Name : ")
    snap_descr = input("Description : ")
    snap_bool = None
    while True:
        snap_bool = input("Consistent ? [True / False] : ")
        if snap_bool in ["True", "False"]:
            break
        else:
            print("\nChoose either 'True' or 'False'\n")
    data = {
        "snapType": snap_type,
        "name": snap_name,
        "description": snap_descr,
        "consistent": snap_bool
    }

    return (data, endpoint)

def restore(args, endpoint):
   pass 
