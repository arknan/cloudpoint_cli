#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import argparse
import argcomplete
import api
import sys

gets_dict = {
    "ad-config" : "idm/config/ad",
    "agents" : "agents/",
    "assets" : "assets/",
    "classification-tags" : "classifications/tags",
    "granules" : "granules",
    "jointokens" : "jointokens/",
    "licenses" : "licenses/",
    "plugins" : "plugins/",
    "policies" : "policies/",
    "replication" : "replication/",
    "report-types" : "report-types/",
    "reports" : "reports/",
    "roles" : "authorization/role",
    "schedules" : "schedules/",
    "tasks" : "tasks/",
    "telemetry" : "telemetry/",
    "users" : "idm/user/",
    "version" : "version"
}

EXIT_1 = "\nERROR : Argument 'snapshots' requires -i flag for 'ASSET_ID'\n\
Expected Command Format : cldpt show assets -i <ASSET_ID> snapshots\n"

EXIT_2 = "\nERROR : Granules can only be listed for asset snapshots\n\
Please enter a valid 'SNAP_ID' and 'ASSET_ID'\nExpected Command Format : \
cldpt show assets -i <ASSET_ID> snapshots -i <SNAP_ID> granules\n"

EXIT_3 = "\nERROR : Unknown option passed\n"

def create_parser() :


    parser_main = argparse.ArgumentParser(epilog="""\n \nFor help information \
related to each sub-command/positional argument, \nUse "-h" or "--help" \
at the end of that sub-command \n \nExamples : "cldpt create -h", \
"cldpt show assets -i <ASSET_ID> --help" \n """,\
    formatter_class=argparse.RawTextHelpFormatter)
    subparser_main = parser_main.add_subparsers(dest='command')

    parser_s = subparser_main.add_parser("show", help="show operations")
    subparser_s = parser_s.add_subparsers(dest="sub_command")

    parser_s_r = subparser_s.add_parser("reports")
    parser_s_r.add_argument("-i", "--id", dest="report_id",\
    help="Get information on a specific report ID")

    parser_s_a = subparser_s.add_parser("assets")
    parser_s_a.add_argument("-i", "--id", dest="asset_id",\
    help="Get information on a specific asset ID")

    subparser_s_a = parser_s_a.add_subparsers(dest="asset_command")
    parser_s_a_s = subparser_s_a.add_parser ("snapshots")
    parser_s_a_s.add_argument("-i","--id", dest="snap_id",\
    help="Get information on a specific snapshot ID")

    subparser_s_a_s = parser_s_a_s.add_subparsers(dest="snapshot_command")
    parser_s_a_s_g = subparser_s_a_s.add_parser("granules")
    parser_s_a_s_g.add_argument("-i", "--id", dest="granule_id",\
    help="Get information on a specific snapshot granule ID")

    parser_a = subparser_main.add_parser("authenticate", \
    help="Login to CloudPoint ; Required for doing any other operation")

    parser_c = subparser_main.add_parser("create",\
    help="Create any information within CloudPoint")

    return parser_main

def interface(args) :

    def check_attr(args, attr) :
        try :
            if hasattr(args, attr) :
                if getattr(args, attr) :
                    return True
        except NameError:
            return False
        else :
            return False

    method_dict = {
        "show" : "gets",
        "create" : "posts",
        "authenticate" : "authenticate"
    }

    endpoint = []
    
    if args.command == "show" :
        if args.sub_command == "assets" :
            endpoint.append(gets_dict[args.sub_command])
            if (check_attr(args, 'asset_id')):
                endpoint.append(args.asset_id)
            if (check_attr(args, 'asset_command') ) and (args.asset_command == "snapshots") :
                if (check_attr(args, 'asset_id')) :
                    endpoint.append(args.asset_command)
                    if (check_attr(args, 'snap_id')) :
                        endpoint.append(args.snap_id)
                else :
                    print(EXIT_1)
                    sys.exit(2)
            if (check_attr(args, 'snapshot_command') ) and (args.snapshot_command == "granules") :
                if (check_attr(args, 'asset_id')) and (check_attr(args, 'snap_id')) :
                    endpoint.append(args.snapshot_command + '/')
                    if (check_attr(args, 'granule_id')) :
                        endpoint.append(args.granule_id)
                else :
                    print(EXIT_2)
                    sys.exit(3)

        elif args.sub_command == "reports" :
            endpoint.append(gets_dict[args.sub_command])
            if (check_attr(args, 'report_id')) :
                endpoint.append(args.report_id)

        getattr(api.Command(), method_dict[args.command]) ('/'.join(endpoint))

    elif args.command == "authenticate" :
        getattr(api.Command(), method_dict[args.command]) ()
        sys.exit(4)

    elif args.command == "create" :
        getattr(api.Command(), method_dict[args.command]) ()
    else :
        print(EXIT_3)
        sys.exit(5)
        
def main() :
    parser = create_parser()
    argcomplete.autocomplete(parser)
    args = parser.parse_args(sys.argv[1:])
    if len(sys.argv) == 1 :
        parser.print_help()
        sys.exit(-1)
    else :
        interface(args)


if __name__ == "__main__" :
    main()
