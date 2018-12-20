#!/usr/bin/env python3

import json
import os
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

    endpoint = ['/licenses/']
    output = None
    print_args = None

    if args.licenses_command == "add":
        data = add(args)
        output = getattr(api.Command(), 'posts')('/'.join(endpoint), data)

    elif args.licenses_command == 'delete':
        delete(args, endpoint)
        output = getattr(api.Command(), 'deletes')('/'.join(endpoint))

    elif args.licenses_command == 'show':
        print_args = show(args, endpoint)
        output = getattr(api.Command(), 'gets')('/'.join(endpoint))

    else:
        LOG_C.error("No arguments provided for 'licenses'")
        cloudpoint.run(["licenses", "-h"])
        sys.exit(1)

    return output, print_args


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

    print_args = None
    if utils.check_attr(args, 'licenses_show_command'):
        if args.licenses_show_command == "active":
            endpoint.append('/?IsLicenseActive=true')
            print_args = "active"

        elif args.licenses_show_command == "features":
            endpoint.append('/all/features')
            print_args = "features"

    elif utils.check_attr(args, 'license_id'):
        endpoint.append(args.license_id)
        print_args = "license_id"

    else:
        print_args = "show"

    return print_args


def pretty_print(output, print_args, pformat=utils.print_format()):

    try:
        table = texttable.Texttable(max_width=COLUMNS)
        data = json.loads(output)

        if pformat == 'json':
            print(output)
            sys.exit(0)
        else:
            table.set_deco(pformat)

        if print_args == "license_id":
            table.header(["Attribute", "Value"])
            table.set_cols_dtype(['t', 't'])
            ignored = ['FulfillmentId', 'CountPolicy', 'IsLicenseActive',
                       'SerialId', 'SvcPolicy', 'WarnPolicy', 'GracePolicy']
            table.add_row(("License Key ID", list(data.keys())[0]))
            for key, value in sorted(data.items()):
                table.add_rows([(i, j) for i, j in sorted(
                    data[key].items()) if i not in ignored], header=False)

        elif print_args in ['show', 'active']:
            required = ["EndDate", "LicenseState", "ProductEdition"]
            headers = ["License Key ID"]
            rows = sorted(data.keys())
            for i in sorted(data.keys()):
                for key, value in sorted(data[i].items()):
                    if key in required:
                        headers.append(key)
                        rows.append(value)

            table.header(headers)
            table.add_row(rows)

        elif print_args == 'features':
            table.header(["Attribute", "Value"])
            table.set_cols_dtype(['t', 't'])
            for key, value in sorted(data.items()):
                for i, j in sorted(data[key].items()):
                    if i in ['MeterCount', 'MeterType', 'ProductEdition']:
                        table.add_row((i, j))
                    else:
                        table.add_row((i, bool(j)))

        else:
            table.header(["Attribute", "Value"])
            for key, value in sorted(data.items()):
                table.add_rows([(i, j) for i, j in sorted(
                    data[key].items())], header=False)

        if table.draw():
            print(table.draw())

    except KeyboardInterrupt:
        sys.exit(0)

    except Exception:
        LOG_F.critical(traceback.format_exc())
        print(output)
