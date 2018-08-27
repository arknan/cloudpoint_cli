#!/usr/bin/env python3

import json
import os
import sys
from texttable import Texttable
import api
import cloudpoint
import logs

LOG_C = logs.setup(__name__, 'c')
LOG_FC = logs.setup(__name__)


def entry_point(args):

    endpoint = ['/licenses/']

    if args.licenses_command == "add":
        data = add(args)
        output = getattr(api.Command(), 'posts')('/'.join(endpoint), data)

    elif args.licenses_command == 'delete':
        delete(args, endpoint)
        output = getattr(api.Command(), 'deletes')('/'.join(endpoint))

    elif args.licenses_command == 'show':
        show(args, endpoint)
        output = getattr(api.Command(), 'gets')('/'.join(endpoint))

    else:
        LOG_C.error("No arguments provided for 'licenses'")
        cloudpoint.run(["licenses", "-h"])
        sys.exit(1)

    return output


def add(args):

    slf = args.file_name
    contents = None
    if not os.path.isfile(args.file_name):
        LOG_FC.error("File '%s' doesn't exist.", args.file_name)
        LOG_FC.error("Check file name/Ensure that a full path is provided")
        sys.exit(1)

    with open(slf, "r") as slf_file:
        contents = slf_file.read()

    data = {"content": contents}
    return data


def delete(args, endpoint):

    endpoint.append(args.license_id)


def show(args, endpoint):

    if api.check_attr(args, 'licenses_show_command'):
        if args.licenses_show_command == "active":
            endpoint.append('/?IsLicenseActive=true')
        elif args.licenses_show_command == "features":
            endpoint.append('/all/features')

    if api.check_attr(args, 'license_id'):
        endpoint.append(args.license_id)


def pretty_print(args, output):

    try:
        data = json.loads(output)
        table = Texttable()

        if api.check_attr(args, 'license_id'):
            ignored = ['FulfillmentId', 'CountPolicy', 'GracePolicy',
                       'IsLicenseActive', 'SerialId', 'SvcPolicy']
            table.add_row(("License Key ID", args.license_id))
            for k, v in sorted(data.items()):
                table.add_rows([(i, j) for i, j in sorted(
                    data[k].items()) if i not in ignored], header=False)
        else:
            required = ["EndDate", "LicenseState", "ProductEdition"]
            headers = ["License Key ID"]
            rows = sorted(data.keys())
            for i in sorted(data.keys()):
                for k, v in sorted(data[i].items()):
                    if k in required:
                        headers.append(k)
                        rows.append(v)

            table.header(headers)
            table.add_row(rows)

        print(table.draw())
    except KeyError, AttributeError:
        print(output)
