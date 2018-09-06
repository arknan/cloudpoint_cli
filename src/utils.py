#!/usr/bin/environment python3

import configparser
import os
import logs

LOG_C = logs.setup(__name__, 'c')

print_mapping = {
    'json': 'json',
    'unix': 0,
    'minimal': 2,
    'tabular': 15,
}


def check_attr(args, attr):

    try:
        return bool(getattr(args, attr))

    except (NameError, IndexError, KeyError, AttributeError):
        return False


def get_stty_cols():

    ROWS, COLS = os.popen('stty size', 'r').read().split()

    return int(COLS)


def print_format():

    config = configparser.ConfigParser()
    config.read('/root/.cloudpoint_cli.config')
    pformat = None
    try:
        pformat = config['GLOBAL']['print_format']
    except KeyError:
        pass

    if pformat not in print_mapping:
        LOG_C.error('%s in CloudPoint config file is not a valid value',
                    pformat)
        LOG_C.error('Using "tabular" as the default output format')
        pformat = 'tabular'

    return print_mapping[pformat]
