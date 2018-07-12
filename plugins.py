#!/usr/bin/env python3

def plugins(endpoint, args):

    if co.check_attr(args, 'plugin_name'):
        endpoint.append(getattr(args, 'plugin_name'))

    if (co.check_attr(args, 'plugins_command')) and \
       (args.plugins_command == "description"):
        if co.check_attr(args, 'plugin_name'):
            endpoint.append("description")
        else:
            print(co.EXIT_6)
            sys.exit(102)
    elif (co.check_attr(args, 'plugins_command')) and \
         (args.plugins_command == "summary"):
        if co.check_attr(args, 'plugin_name'):
            print("\nSummary cannot be provided for a specific plugin\n")
            sys.exit(12)
        else:
            endpoint.append("summary")

    return endpoint

