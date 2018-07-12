#!/usr/bin/env python3

def tasks(endpoint, args):

    if co.check_attr(args, 'task_id'):
        if co.check_attr(args, 'tasks_command'):
            print("\nYou cannot print summary of a task_id\n")
            sys.exit(8)
        endpoint.append(getattr(args, 'task_id'))

    elif co.check_attr(args, 'tasks_command'):
        endpoint.append('/summary')

    else:
        filters = []
        temp_endpoint = []
        for i in 'run_since', 'limit', 'status', 'taskType':
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


def reports(endpoint, args):

    if co.check_attr(args, 'report_id'):
        endpoint.append(getattr(args, 'report_id'))

    if co.check_attr(args, 'reports_command'):
        if co.check_attr(args, 'report_id'):
            if getattr(args, 'reports_command') == "preview":
                endpoint.append('/preview')
            else:
                endpoint.append('/data')
        else:
            print("\nSpecify a REPORT_ID for getting",
                  getattr(args, 'reports_command'), "\n")
            sys.exit(9)

    return endpoint
