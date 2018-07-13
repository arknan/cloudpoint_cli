#!/usr/bin/env python3

import sys
import api
import constants as co

def entry_point(args):

    endpoint = []
    endpoint.append(co.GETS_DICT[args.command])
    if co.check_attr(args, 'tasks_command'):
        globals()[args.tasks_command](args, endpoint)
    else:
        print("Invalid argument : '{}'".format(args.tasks_command))
        sys.exit(-1)

    print(endpoint)
    output = getattr(api.Command(), co.METHOD_DICT[args.tasks_command])('/'.join(endpoint))
    return output

def show(args, endpoint):


# MAYBE THE TASKS TYPE FILTER ISN'T WORKING ... PLEASE CHECK WHY LATER

    if co.check_attr(args, 'task_id'):
        if co.check_attr(args, 'tasks_show_command'):
            print("\nYou cannot print summary of a specific task\n")
            sys.exit(8)
        endpoint.append(getattr(args, 'task_id'))

    elif co.check_attr(args, 'tasks_show_command'):
        endpoint.append('/summary')

    else:
        filters = []
        temp_endpoint = []
        for i in 'run_since', 'limit', 'status', 'task_type':
            if co.check_attr(args, i):
                filters.append(i)

        if (len(filters) != 0) and (filters[0]):
            temp_endpoint.append('?' + filters[0] + '=' +
                                 getattr(args, filters[0]))
            if len(filters) > 1:
                for j in filters[1:]:
                    temp_endpoint.append('&' + j + '=' + getattr(args, j))
        endpoint.append(''.join(temp_endpoint))

    return endpoint

def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format that makes parsing easier !
    print(data)
