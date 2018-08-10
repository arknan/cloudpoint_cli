#!/usr/bin/env python3

import configparser
import logging
import sys


def setup(mod_name, handler_type='fc'):

    config = configparser.ConfigParser()
    config.read('/root/.cloudpoint_cli.config')
    try:
        log_level = config['GLOBAL']['cli_log_level']
        log_file = config['GLOBAL']['cli_log_file']
    except KeyError:
        print("Please ensure config file has 'cli_log_level' &\
'cli_log_file' values\n")
        sys.exit(1)

    logger = logging.getLogger(mod_name + '_' + handler_type)
    logger.setLevel(getattr(logging, log_level.upper()))

    file_formatter = logging.Formatter(
        '%(asctime)s %(module)s %(levelname)s: %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S')

    console_formatter = logging.Formatter(
        '%(levelname)s : %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, log_level.upper()))
    ch.setFormatter(console_formatter)

    fh = logging.FileHandler(log_file)
    fh.setLevel(getattr(logging, log_level.upper()))
    fh.setFormatter(file_formatter)

    if handler_type == 'c':
        logger.addHandler(ch)
    elif handler_type == 'f':
        logger.addHandler(fh)
    else:
        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger
