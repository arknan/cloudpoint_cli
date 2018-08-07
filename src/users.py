#!/usr/bin/env python3

import sys
from getpass import getpass
import api
import cloudpoint
import constants as co


def entry_point(args):

    endpoint = ['/idm/user/']

    if args.users_command == "create":
        data = create()
        output = getattr(api.Command(), 'posts')('/'.join(endpoint), data)

    elif args.users_command == 'reset_password':
        endpoint.append('/forgotPassword')
        data = reset_password()
        output = getattr(api.Command(), 'posts')('/'.join(endpoint), data)
        print("\nPassword has been successfully reset\n")

    elif args.users_command == "show":
        show(args, endpoint)
        output = getattr(api.Command(), 'gets')('/'.join(endpoint))

    else:
        print("No arguments provided for 'users'\n")
        cloudpoint.run(["users", "-h"])
        sys.exit(-1)

    return output


# def create(args, endpoint):
def create():

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


def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format
    print(data)


def reset_password():

    # API endpoint is messed up .. this doesn't work either :(
    print("\nPlease enter the following details for the \
user whose password needs to be changed\n")
    email_addr = input("Email Address : ")
    new_passwd = getpass("New Password : ")

    data = {
        "email": email_addr,
        "newPassword": new_passwd
    }

    return data


def show(args, endpoint):
    if co.check_attr(args, 'user_id'):
        endpoint.append(args.user_id)
