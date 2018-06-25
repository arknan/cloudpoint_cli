#!/usr/bin/env python3

import constants as co


def roles(args, endpoint):

    if co.check_attr(args, 'role_id'):
        endpoint.append('/' + args.role_id)
    else:
        role_id = input("Enter role id of the role you want to delete : ")
        endpoint.append('/' + role_id)

    return endpoint
