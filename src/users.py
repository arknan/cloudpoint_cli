#!/usr/bin/env python3

import json
import sys
from getpass import getpass
import texttable
import api
import cloudpoint
import logs
import utils

COLUMNS = utils.get_stty_cols()
LOG_C = logs.setup(__name__, 'c')
LOG_FC = logs.setup(__name__)


def entry_point(args):

    endpoint = ['/idm/user/']

    if args.users_command == "create":
        data = create()
        output = getattr(api.Command(), 'posts')('/'.join(endpoint), data)

    elif args.users_command == 'reset_password':
        endpoint.append('/forgotPassword')
        data = reset_password()
        output = getattr(api.Command(), 'posts')('/'.join(endpoint), data)
        LOG_FC.info("Password reset successful for user '%s'",
                    data['email'])

    elif args.users_command == "show":
        print_args = show(args, endpoint)
        output = getattr(api.Command(), 'gets')('/'.join(endpoint))
        pretty_print(output, print_args)

    else:
        LOG_C.error("No arguments provided for 'users'")
        cloudpoint.run(["users", "-h"])
        sys.exit(1)

    return output


# def create(args, endpoint):
def create():

    LOG_C.warning("User must be verifiable by both LDAP and SMTP")
    first_name = input("Firstname : ")
    last_name = input("Lastname : ")
    email_addr = input("Email : ")

    data = {
        "lastName": last_name,
        "email": email_addr,
        "firstName": first_name
    }

    return data


def reset_password():

    # API endpoint is messed up .. this doesn't work either :(
    LOG_C.info("Please enter the following details of the user :")
    email_addr = input("Email Address : ")
    new_passwd = getpass("New Password : ")

    data = {
        "email": email_addr,
        "newPassword": new_passwd
    }

    return data


def show(args, endpoint):

    print_args = None
    if utils.check_attr(args, 'user_id'):
        endpoint.append(args.user_id)
        print_args = 'user_id'
    else:
        print_args = 'show'

    return print_args


def pretty_print(output, print_args):

    try:
        data = json.loads(output)
        table = texttable.Texttable(max_width=COLUMNS)
        table.set_deco(texttable.Texttable.HEADER)

        if print_args == 'user_id':
            ignored = ["links", "uri"]
            table.add_rows(
                [(k, v) for k, v in sorted(data.items()) if k not in ignored],
                header=False)
        else:
            required = ["id", "email"]
            for i, _ in enumerate(data):
                table.header(sorted(required))
                table.add_row(
                    [v for k, v in sorted(data[i].items()) if k in required])

        if table.draw():
            print(table.draw())

    except(KeyError, AttributeError, TypeError, NameError, texttable.ArraySizeError, json.decoder.JSONDecodeError):
        print(output)
