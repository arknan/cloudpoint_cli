#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import argparse
import argcomplete

def create_parser():
    parser_reports = argparse.ArgumentParser()
    parser_reports.add_argument("-a", help="Hello from reports module !")

    return parser_reports

def entry_point(args):
#    print("You sent : ", args)
    parser_main = create_parser()
    argcomplete.autocomplete(parser_main)
    final = parser_main.parse_args(args)
    print(final)

if __name__ == "__main__":
    print("main")
