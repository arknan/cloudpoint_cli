#!/usr/bin/environment python3

import configparser
import os

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
    pformat = 'minimal'
    try:
        pformat = config['GLOBAL']['print_format']
    except KeyError:
        pass

    if pformat in print_mapping:
        return print_mapping[pformat]
    else:
        return print_mapping['minimal']
