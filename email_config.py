#!/usr/bin/env python3

import sys
import api
import constants as co


def entry_point(args):

    endpoint = []
    if args.email_config_command == 'show':
        endpoint.append(co.GETS_DICT[args.command])
        # show(args, endpoint)
        output = getattr(
            api.Command(), co.METHOD_DICT[args.email_config_command])(
                '/'.join(endpoint))
    elif args.email_config_command == 'create':
        # create(args, endpoint)
        create()
    else:
        print("Invalid argument : '{}'".format(args.email_config_command))
        sys.exit(-1)

    return output


# def show(args, endpoint):
def show():
    # There is no work needed here, since our GETS_DICT provides
    # the whole endpoint ... retaining this for future ?
    pass


# def create(args, endpoint):
def create():

    # This doesn't seem to work currently,
    # maybe the data format is wrong ! need to check with ENGG
    """
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

    return (data, endpoint)
    """
    print("Not implemented")
    sys.exit(-1)


def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format
    print(data)
