#!/usr/bin/env python3

def replication(endpoint, args):

    if co.check_attr(args, 'policy_name'):
        endpoint.append(getattr(args, 'policy_name'))
    if co.check_attr(args, 'replication_command'):
        if co.check_attr(args, 'policy_name'):
            endpoint.append('/rules/')
        else:
            print("Mention a policy name to get replication rules\n")
            sys.exit(-1)

    return endpoint
