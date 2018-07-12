#!/usr/bin/env python3

def agents(endpoint, args):

    detail = (args.show_command)[:-1] + '_id'
    if co.check_attr(args, detail):
        endpoint.append(getattr(args, detail))

    if (co.check_attr(args, 'agents_command')) and \
       (args.agents_command == "plugins"):
        if co.check_attr(args, detail):
            endpoint.append("plugins/")
            if co.check_attr(args, 'plugin_name'):
                endpoint.append(args.plugin_name)
        else:
            print(co.EXIT_5)
            sys.exit(101)
        if co.check_attr(args, "configured_plugin_name"):
            endpoint.append(args.configured_plugin_name)
    elif (co.check_attr(args, 'agents_command')) and \
         (args.agents_command == "summary"):
        if co.check_attr(args, detail):
            print("\nSummary cannot be provided for a specific agent\n")
            sys.exit(11)
        else:
            endpoint.append("summary")

    return endpoint
