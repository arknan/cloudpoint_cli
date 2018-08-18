#!/usr/bin/env python3

import configparser
import logging
import os
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

    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(console_formatter)

    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    open(log_file, 'a').close()

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(getattr(logging, log_level.upper()))
    file_handler.setFormatter(file_formatter)

    if handler_type == 'c':
        logger.addHandler(console_handler)
    elif handler_type == 'f':
        logger.addHandler(file_handler)
    else:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
