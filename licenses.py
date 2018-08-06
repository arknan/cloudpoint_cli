#!/usr/bin/env python3

import sys
import os
import api
import cldpt
import constants as co


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
        output = getattr(
            api.Command(), co.METHOD_DICT[args.licenses_command])(
                '/'.join(endpoint))
    else:
        print("No arguments provided for 'licenses'\n")
        cldpt.run(["licenses", "-h"])
        sys.exit(-1)

    return output


def add(args):

    slf = args.file_name
    contents = None
    if not os.path.isfile(args.file_name):
        print("File {} doesn't exist.".format(args.file_name))
        print("Check file name or ensure that a full path is provided")
        sys.exit(-1)

    with open(slf, "r") as slf_file:
        contents = slf_file.read()

    data = {"content": contents}
    return data


def delete(args, endpoint):

    endpoint.append(args.license_id)


def show(args, endpoint):

    if co.check_attr(args, 'licenses_show_command'):
        if args.licenses_show_command == "active":
            endpoint.append('/?IsLicenseActive=true')
        elif args.licenses_show_command == "features":
            endpoint.append('/all/features')

    if co.check_attr(args, 'license_id'):
        endpoint.append(getattr(args, 'license_id'))


def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format
    print(data)
