#!/usr/bin/env python3

import json
import sys
from getpass import getpass
import api
import cldpt
import constants as co


def entry_point(args):

    endpoint = []
    if args.email_config_command == 'show':
        endpoint.append(co.GETS_DICT['email_config'])
        # show(args, endpoint)
        output = getattr(
            api.Command(), co.METHOD_DICT[args.email_config_command])(
                '/'.join(endpoint))
    elif args.email_config_command == 'create':
        endpoint.append(co.GETS_DICT['email_config'])
        data = create(args)
        output = getattr(
            api.Command(), 'puts')('/'.join(endpoint), data)

    elif args.email_config_command == 'delete':
        endpoint.append(co.GETS_DICT['email_config'])
        getattr(
            api.Command(), 'deletes')('/'.join(endpoint))
        output = 'Email Configuration has been deleted'

    else:
        print("No arguments provided for 'email_config'\n")
        cldpt.run(["email_config", "-h"])
        sys.exit(-1)

    return output


# def show(args, endpoint):
def show():
    # There is no work needed here, since our GETS_DICT provides
    # the whole endpoint ... retaining this for future ?
    pass


# def create(args, endpoint):
def create(args):

    if co.check_attr(args, 'email_config_create_command'):
        if args.email_config_create_command == 'aws_ses':
            print("\nPlease enter the following AWS details :\n")
            aws_ak = input("Access Key :")
            aws_sk = getpass("Secret Key :")
            aws_region = input("Region :")
            print("\nPlease enter the sender's email address")
            aws_email = input("Sender Email : ")

            data = {
                "type": "awsses",
                "senderEmail": aws_email
            }
            data["data"] = json.dumps({
                "region": aws_region,
                "accessKey": aws_ak,
                "secretKey": aws_sk
            })

        elif args.email_config_create_command == 'send_grid':
            print("\nPlease enter the sender's email address")
            sg_email = input("Sender Email : ")
            print("\nPlease enter the API key for SendGrid\n")
            sg_apikey = getpass("API Key :")

            data = {
                "type": "sendgrid",
                "senderEmail": sg_email
            }
            data["data"] = json.dumps({
                "apiKey": sg_apikey
            })

        elif args.email_config_create_command == 'smtp':
            print("\nPlease enter the IP address of SMTP server")
            smtp_ip = input("IP Address : ")
            print("\nPlease enter the port used by SMTP")
            smtp_port = input("Port (25) : ")
            if not smtp_port:
                smtp_port = 25
            print("\nPlease enter SMTP credentials\n")
            print("[Hit enter to skip if anonymous authentication is used\n]")
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
            }
            if auth:
                data["data"] = json.dumps({
                    "host": smtp_ip,
                    "port": smtp_port,
                    "authentication": True,
                    "username": smtp_user,
                    "password": smtp_passwd,
                })
            else:
                data["data"] = json.dumps({
                    "host": smtp_ip,
                    "port": smtp_port,
                    "authentication": False
                })
        else:
            print("INTERNAL ERROR")
            sys.exit()

    else:
        cldpt.run(["email_config", "create", "-h"])
        sys.exit()

    return data


def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format
    print(data)
