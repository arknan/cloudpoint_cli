#!/usr/bin/env python3

import sys
import api
import constants as co

def entry_point(args):

    endpoint = []
    if args.users_command == "show":	
        endpoint.append(co.GETS_DICT[args.command])
        show(args, endpoint)
        output = getattr(api.Command(), co.METHOD_DICT['show'])('/'.join(endpoint))

    elif args.users_command == "create":
        data = None
        endpoint.append(co.POSTS_DICT[args.user])
        data = create(args, endpoint)
        output = getattr(api.Command(), co.METHOD_DICT['create'])('/'.join(endpoint), data)

    elif args.users_command == 'reset_password':
        endpoint.append(co.POSTS_DICT['reset_password'])
        data = modify(args, endpoint)
        output = getattr(api.Command(), co.METHOD_DICT['modify'])('/'.join(endpoint))

    else:
        print("Invalid argument : '{}'".format(args.users_command))
        sys.exit(-1)

    return output

def show(args, endpoint):
    if co.check_attr(args, 'user_id'):
        endpoint.append(args.user_id)

def create(args, endpoint):

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

def modify():
    # API endpoint is messed up .. this doesn't work either :(
    """
    email_addr = input("Email : ")
    new_passwd = getpass("New Password : ")

    data = {
        "email": email_addr,
        "newPassword": new_passwd
    }

    return data
    """
    print("Not implemented")
    sys.exit(-1)


def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format that makes parsing easier !
    print(data)
