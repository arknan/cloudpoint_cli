#!/usr/bin/env python3

import datetime
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


def entry_point(args):

    endpoint = ['/tasks/']
    output = None
    print_args = None
    if args.tasks_command == 'delete':
        delete(args, endpoint)
        output = getattr(api.Command(), 'deletes')('/'.join(endpoint))

    elif args.tasks_command == 'show':
        print_args = show(args, endpoint)
        output = getattr(api.Command(), 'gets')('/'.join(endpoint))

    else:
        LOG_C.error("No arguments provided for 'tasks'")
        cloudpoint.run(["tasks", "-h"])
        sys.exit(1)

    return output, print_args


def delete(args, endpoint):

    # STATUS based deletion is failing :( Need to check with Engineering

    if utils.check_attr(args, 'task_id'):
        endpoint.append(args.task_id)

    elif utils.check_attr(args, 'status'):
        temp_endpoint = ['?status=' + args.status]
        if utils.check_attr(args, 'older_than'):
            temp_endpoint.append('&olderThan=' + args.older_than)

        endpoint.append(''.join(temp_endpoint))
    else:
        LOG_C.error("Invalid option for 'delete'")
        cloudpoint.run(["tasks", "delete", "-h"])


def show(args, endpoint):

    # MAYBE THE TASKS TYPE FILTER ISN'T WORKING ... PLEASE CHECK WHY LATER

    print_args = None
    if utils.check_attr(args, 'task_id'):
        if utils.check_attr(args, 'tasks_show_command'):
            LOG_C.error("You cannot get summary of a specific task")
            sys.exit(1)

        endpoint.append(getattr(args, 'task_id'))
        print_args = "task_id"

    elif utils.check_attr(args, 'tasks_show_command'):
        endpoint.append('/summary')
        print_args = "summary"

    else:
        print_args = "show"
        filters = []
        temp_endpoint = []
        for i in 'run_since', 'limit', 'status', 'task_type':
            if utils.check_attr(args, i):
                filters.append(i)

        if (filters) and (filters[0]):
            temp_endpoint.append('?' + filters[0] + '=' +
                                 getattr(args, filters[0]))
            if len(filters) > 1:
                for j in filters[1:]:
                    temp_endpoint.append('&' + j + '=' + getattr(args, j))

        endpoint.append(''.join(temp_endpoint))

    return print_args


def pretty_print(output, print_args, pformat=utils.print_format()):

    try:
        data = json.loads(output)
        table = texttable.Texttable(max_width=COLUMNS)

        if pformat == 'json':
            print(output)
            sys.exit(0)
        else:
            table.set_deco(pformat)

        if print_args == "task_id":
            print(output)
            table.header(["Attribute", "Value"])
            table.set_cols_dtype(['t', 't'])
            for key, value in sorted(data.items()):
                if key == 'ctime':
                    table.add_row((key.capitalize(),
                                   datetime.datetime.fromtimestamp(value)))
                elif key == 'asset':
                    pass
                else:
                    table.add_row((key.capitalize(), value))

        elif print_args == 'show':
            required = ["name", "status", "taskid"]
            table.header([i.capitalize() for i in sorted(required)])

            for i, _ in enumerate(data):
                table.add_row(
                    [value for key, value in sorted(data[i].items())
                     if key in required])

        else:
            table.header(("Attribute", "Value"))
            table.add_rows(
                [(key, value) for key, value in sorted(data.items())],
                header=False)

        if table.draw():
            print(table.draw())

    except(KeyError, AttributeError, TypeError, NameError,
           texttable.ArraySizeError, json.decoder.JSONDecodeError):
        LOG_F.critical(traceback.format_exc())
        print(output)
