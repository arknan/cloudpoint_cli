#!/usr/bin/env python3

import api


def entry_point(args):
    endpoint = ['/version']
    output = getattr(api.Command(), 'gets')('/'.join(endpoint))

    return output


def pretty_print(data):
    # This function has to be tailor suited for each command's output
    # Since all commands don't have a standard output format
    print(data)
