#!/usr/bin/env python3

from getpass import getpass
import json
import sys
import traceback
import texttable
import api
import cloudpoint
import logs
import utils

COLUMNS = utils.get_stty_cols()
LOG_C = logs.setup(__name__, 'c')
LOG_F = logs.setup(__name__, 'f')
LOG_FC = logs.setup(__name__)


def entry_point(args):

    endpoint = ['/email/config']
    output = None
    print_args = None

    if utils.check_attr(args, 'email_config_command'):
        if args.email_config_command == 'show':
            print_args = show()
            output = getattr(api.Command(), 'gets')('/'.join(endpoint))

        elif args.email_config_command == 'create':
            data = create(args)
            output = getattr(api.Command(), 'puts')('/'.join(endpoint), data)

        elif args.email_config_command == 'delete':
            getattr(api.Command(), 'deletes')('/'.join(endpoint))
            output = 'Email Configuration has been deleted'

        else:
            LOG_FC.critical("INTERNAL ERROR 1 IN '%s'", __file__)
            sys.exit(1)

    else:
        LOG_C.error("No arguments passed for email_config")
        cloudpoint.run(["email_config", "-h"])
        sys.exit(1)

    return output, print_args


def show():
    # There is no work needed here, since our GETS_DICT provides
    # the whole endpoint ... retaining this for future ?
    pass


def create(args):

    if utils.check_attr(args, 'email_config_create_command'):
        if args.email_config_create_command == 'aws_ses':
            LOG_C.info("Please enter the following AWS details :\n")
            aws_ak = input("Access Key :")
            aws_sk = getpass("Secret Key :")
            aws_region = input("Region :")
            LOG_C.info("Please enter the sender's email address")
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
            LOG_C.info("Please enter the sender's email address")
            sg_email = input("Sender Email : ")
            LOG_C.info("\nPlease enter the API key for SendGrid\n")
            sg_apikey = getpass("API Key :")

            data = {
                "type": "sendgrid",
                "senderEmail": sg_email
            }
            data["data"] = json.dumps({
                "apiKey": sg_apikey
            })

        elif args.email_config_create_command == 'smtp':
            LOG_C.info("Please enter the IP address of SMTP server")
            smtp_ip = input("IP Address : ")
            LOG_C.info("\nPlease enter the port used by SMTP")
            smtp_port = input("Port (25) : ")
            if not smtp_port:
                smtp_port = 25
            LOG_C.info("Please enter SMTP credentials")
            LOG_C.info(
                "[Hit enter to skip if anonymous authentication is used\n]")
            smtp_user = input("User name : ")
            smtp_passwd = None
            auth = False
            if smtp_user:
                auth = True
                smtp_passwd = getpass("Password: ")
            LOG_C.info("\nPlease enter the smtp sender email address")
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
            LOG_FC.critical("INTERNAL ERROR 2 IN '%s'", __file__)
            sys.exit(1)

    else:
        LOG_C.error("No arguments provided for 'create'")
        cloudpoint.run(["email_config", "create", "-h"])
        sys.exit(1)

    return data


def pretty_print(output, print_args):

    try:
        table = texttable.Texttable(max_width=COLUMNS)
        data = json.loads(output)
        pformat = utils.print_format()

        if pformat == 'json':
            print(output)
            sys.exit(0)
        else:
            table.set_deco(pformat)

        data_data = json.loads(data['data'])
        print_dict = {}

        for k, v in sorted(data.items()):
            if k not in ['data', 'configKey']:
                print_dict[k] = v

        for k, v in sorted(data_data.items()):
            if k not in ['authentication']:
                print_dict[k] = v

        table.header([k for k, v in sorted(print_dict.items())])
        table.add_row([v for k, v in sorted(print_dict.items())])

        if table.draw():
            print(table.draw())

    except(KeyError, AttributeError, TypeError, NameError,
           texttable.ArraySizeError, json.decoder.JSONDecodeError):
        LOG_F.critical(traceback.format_exc())
        print(output)
