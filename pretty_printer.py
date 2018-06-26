#!/usr/bin/env python3

import os
import json
from constants import DONT_PRINT, COLUMNS


def chomp(data):
    final = data.replace('\n', '').replace(' ', '')
    return final


def cover():
    print('+', end='')
    print('=' * int(COLUMNS - 2), end='')
    print('+', end='')


def maxlengths(value):

    len_val = 0
    for i in value:
        if len(i) > len_val:
            len_val = len(i)

    return len_val


def print_it_assets(data, endpoint):
    endpt_len = len(endpoint)
    if endpt_len == 1:
        print_it_general(data["items"])
    elif endpt_len == 2:
        print_it_general(data)


def print_it_general(data, col_len=0, nested=False):

    if isinstance(data, dict):
        col_len = maxlengths(sorted(data))
        for key, value in sorted(data.items()):
            if key in DONT_PRINT:
                pass
            else:
                if nested:
                    print('{1:>{2}}{0:<{2}}{1}'.format(
                        key, '|', col_len), end='')
                else:
                    print('{1}{0:<{2}}{1}'.format(key, '|', col_len), end='')

                if (isinstance(value, dict)) and (value):
                    print('\n')
                    print_it_general(value, col_len, True)
                else:
                    print('{0}\n'.format(str(value)), end='')
                print('-' * COLUMNS)
        if not nested:
            print('=' * COLUMNS)

    elif isinstance(data, list):
        for i in data:
            if isinstance(i, dict):
                print_it_general(i)
            else:
                print(i)
    else:
        print(data)


def print_nested(data, endpoint):

    final = None
    type_error = False

    cover()
    try:
        final = json.loads(data)
    except (TypeError, json.decoder.JSONDecodeError):
        type_error = True

    if type_error:
        if "errorMessage" in data:
            print_it_general(data)
            cover()
            os.sys.exit(0)
        else:
            print(data)
    else:
        if "assets/" in endpoint:
            print_it_assets(final, endpoint)
        else:
            print_it_general(final)
    cover()
