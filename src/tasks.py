#!/usr/bin/env python3

import json
import sys
import texttable
import api
import cloudpoint
import logs

LOG_C = logs.setup(__name__, 'c')


def entry_point(args):

    endpoint = ['/tasks/']
    if args.tasks_command == 'delete':
        delete(args, endpoint)
        output = getattr(api.Command(), 'deletes')('/'.join(endpoint))

    elif args.tasks_command == 'show':
        show(args, endpoint)
        output = getattr(api.Command(), 'gets')('/'.join(endpoint))

    else:
        LOG_C.error("No arguments provided for 'tasks'")
        cloudpoint.run(["tasks", "-h"])
        sys.exit(1)

    return output


def delete(args, endpoint):

    # STATUS based deletion is failing :( Need to check with Engineering

    if api.check_attr(args, 'task_id'):
        endpoint.append(args.task_id)

    elif api.check_attr(args, 'status'):
        temp_endpoint = ['?status=' + args.status]
        if api.check_attr(args, 'older_than'):
            temp_endpoint.append('&olderThan=' + args.older_than)

        endpoint.append(''.join(temp_endpoint))
    else:
        LOG_C.error("Invalid option for 'delete'")
        cloudpoint.run(["tasks", "delete", "-h"])


def show(args, endpoint):

    # MAYBE THE TASKS TYPE FILTER ISN'T WORKING ... PLEASE CHECK WHY LATER

    if api.check_attr(args, 'task_id'):
        if api.check_attr(args, 'tasks_show_command'):
            LOG_C.error("You cannot get summary of a specific task")
            sys.exit(1)

        endpoint.append(getattr(args, 'task_id'))

    elif api.check_attr(args, 'tasks_show_command'):
        endpoint.append('/summary')

    else:
        filters = []
        temp_endpoint = []
        for i in 'run_since', 'limit', 'status', 'task_type':
            if api.check_attr(args, i):
                filters.append(i)

        if (filters) and (filters[0]):
            temp_endpoint.append('?' + filters[0] + '=' +
                                 getattr(args, filters[0]))
            if len(filters) > 1:
                for j in filters[1:]:
                    temp_endpoint.append('&' + j + '=' + getattr(args, j))

        endpoint.append(''.join(temp_endpoint))


def pretty_print(args, output):

    try:
        data = json.loads(output)
        table = texttable.Texttable()

        if args.task_id:
            table.add_rows([(k, v) for k, v in sorted(data.items())], header=False)
        else:
            required = ["name", "status", "taskid"]
            table.header(sorted(required))

            for i, _ in enumerate(data):
                table.add_row(
                    [v for k, v in sorted(data[i].items()) if k in required])

        if table.draw():
            print(table.draw())

    except(KeyError, AttributeError, TypeError, NameError, texttable.ArraySizeError, json.decoder.JSONDecodeError):
        print(output)
