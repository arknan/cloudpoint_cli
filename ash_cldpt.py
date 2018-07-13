#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import sys
import argparse
import argcomplete
import agents
import reports, assets, agents, plugins, licenses, tasks, replication
import privileges, roles, users, policies, email_config, ldap_config


def create_parser():

    """ MAIN PARSER """
    parser_main = argparse.ArgumentParser()
    subparser_main = parser_main.add_subparsers(
	   dest='command', metavar='<positional argument>')

    """ AGENT RELATED PARSING """
    parser_agents = subparser_main.add_parser(
        "agents", help="Agent related operations")
    subparser_agents = parser_agents.add_subparsers(
        dest="agents_command", metavar='<agent argument>')
    # SHOW [GET] PARSING
    parser_agents_show = subparser_agents.add_parser(
        "show", help="Show agent related information")
    parser_agents_show.add_argument(
        "-i", "--agent-id", help="Show information related to a specific agent")
    subparser_agents_show = parser_agents_show.add_subparsers(
        dest="agents_show_command", metavar='<positional argument>')
    parser_agents_show_plugins = subparser_agents_show.add_parser(
        "plugins", help="Show related plugins for an agent")
    parser_agents_show_plugins.add_argument(
        "-i", "--plugin-name", dest="configured_plugin_name",
        help="Show plugin information for a specific agent plugin")
    parser_agents_show_summary = subparser_agents_show.add_parser(
        "summary", help="Show summary of agents")
    # CREATE [PUT/POST] PARSING

    """ ASSET RELATED PARSING """
    parser_assets = subparser_main.add_parser(
        "assets", help="Asset releated operations")
    subparser_assets = parser_assets.add_subparsers(
        dest="assets_command", metavar='<asset argument>')
    # SHOW [GET] PARSING
    parser_assets_show = subparser_assets.add_parser(
        "show", help="Show assets related information")
    parser_assets_show.add_argument(
        "-i", "--asset-id", help="Show information related to a specifici asset")
    subparser_assets_show = parser_assets_show.add_subparsers(
        dest="assets_show_command", metavar='<positional argument>')
    parser_assets_show_snapshots = subparser_assets_show.add_parser(
        "snapshots", help="Show related snapshots for an asset")
    parser_assets_show_snapshots.add_argument(
        "-i", "--snapshot-id", help="Show snapshot information for a specific snapshot")
    subparser_assets_show_snapshots = parser_assets_show_snapshots.add_subparsers(
        dest="snapshots_command", metavar='<positional argument>')
    parser_assets_show_snapshots_granules = subparser_assets_show_snapshots.add_parser(
        "granules", help="Show granules for a snapshot of an asset")
    parser_assets_show_snapshots_granules.add_argument(
        "-i", "--granule-id", help="Show information on a particular granule")
    parser_assets_show_snapshots_restore_targets = subparser_assets_show_snapshots.add_parser(
        "restore-targets", help="Show restore target locations for a specific snapshot asset")
    parser_assets_show_policies = subparser_assets_show.add_parser(
        "policies", help="Show policy information for an asset")
    parser_assets_show_summary = subparser_assets_show.add_parser(
        "summary", help="Show summary of assets")
    # CREATE [PUT/POST] PARSING
    parser_assets_create = subparser_assets.add_parser(
        "create", help="Create asset related information in CloudPoint")
    subparser_assets_create = parser_assets_create.add_subparsers(
        dest="assets_create_command", metavar='<positional argument>')
    parser_assets_create_snapshot = subparser_assets_create.add_parser(
        "snapshot", help="Take snapshots of assets")
    parser_assets_create_snapshot.add_argument(
        "-i", "--asset-id", help="Provide an ASSET_ID to snap")
    parser_assets_create_replicas = subparser_assets_create.add_parser(
        "replicas", help="Replicate Existing snapshots")
    parser_assets_create_replicas.add_argument(
        "-i", "--snapshot-id", help="Provide a SNAPSHOT_ID to replicate")
    parser_assets_restore = subparser_assets.add_parser(
        "restore", help="Restore snapshots")
    parser_assets_restore.add_argument(
        "-i", "--snapshot-id", help="Provide a SNAPSHOT_ID to restore")

    """ AUTHENTICATION RELATED PARSING """
    parser_authenticate = subparser_main.add_parser(
        "authenticate", help="Login to CloudPoint")

    """ EMAIL RELATED PARSING """
    parser_email_config = subparser_main.add_parser(
        "email_config", help="SMTP related operations")
    subparser_email_config = parser_email_config.add_subparsers(
        dest="email_config_command", metavar='<positional argument>')
    # SHOW [GET] PARSING
    parser_email_config_show = subparser_email_config.add_parser(
        "show", help="Show SMTP related details")
    # CREATE [PUT/POST] PARSING
    parser_email_config_create = subparser_email_config.add_parser(
        "create", help="Add email/smtp related settings")
    subparser_email_config_create = parser_email_config_create.add_subparsers(
        dest="email_config_create_command", metavar='<positional argument>')
    parser_email_config_create_email_config = subparser_email_config_create.add_parser(
        "email_config", help="Add Email configuration")

    """ LDAP RELATED PARSING """
    parser_ldap_config = subparser_main.add_parser(
        "ldap_config", help="LDAP related operations")
    subparser_ldap_config = parser_ldap_config.add_subparsers(
        dest="ldap_config_command", metavar='<positional argument>')
    # SHOW [GET] PARSING
    parser_ldap_config_show = subparser_ldap_config.add_parser(
        "show", help="Show LDAP related details")
    # CREATE [PUT/POST] PARSING

    """ LICENSE RELATED PARSING """
    parser_licenses = subparser_main.add_parser(
        "licenses", help="Licensing related operations")
    subparser_licenses = parser_licenses.add_subparsers(
        dest="licenses_command", metavar='<positional argument>')
    # SHOW [GET] PARSING
    parser_licenses_show = subparser_licenses.add_parser(
        "show", help="Show licensing related information")
    parser_licenses_show.add_argument(
        "-i", "--license-id", dest="license_id",
        help="Show information on a specific license id")
    subparser_licenses_show = parser_licenses_show.add_subparsers(
        dest="licenses_show_command", metavar='<positional argument>')
    parser_licenses_show_active = subparser_licenses_show.add_parser(
        "active", help="Show information on all active licenses")
    parser_licenses_show_features = subparser_licenses_show.add_parser(
        "features", help="Show information on all licensed features")
    # CREATE [PUT/POST] PARSING


    """ PLUGIN RELATED PARSING """
    parser_plugins = subparser_main.add_parser(
        "plugins", help="Plugin related operations")
    subparser_plugins = parser_plugins.add_subparsers(
        dest="plugins_command", metavar='<positional argument>')
    # SHOW [GET] PARSING
    parser_plugins_show = subparser_plugins.add_parser(
        "show", help="Show plugin related information")
    parser_plugins_show.add_argument(
        "-i", "--plugin-name", dest="available_plugin_name",
        help="Show information on a specific available plugin")
    subparser_plugins_show = parser_plugins_show.add_subparsers(
        dest="plugins_show_command", metavar='<positional argument>')
    parser_plugins_show_description = subparser_plugins_show.add_parser(
        "description", help="Get plugin description for a specific plugin name")
    parser_plugins_show_summary = subparser_plugins_show.add_parser(
        "summary", help="Show summary information for plugins")
    # CREATE [PUT/POST] PARSING

    """ POLICY RELATED PARSING """
    parser_policies = subparser_main.add_parser(
        "policies", help="Policy related operations")
    subparser_policies = parser_policies.add_subparsers(
        dest="policies_command", metavar='<positional argument>')
    # SHOW [GET] PARSING
    parser_policies_show = subparser_policies.add_parser(
        "show", help="Show policy related information")
    parser_policies_show.add_argument(
        "-i", "--policy-id", help="Show information on a particular policy")
    # CREATE [PUT/POST] PARSING
    parser_policies_create = subparser_policies.add_parser(
        "create", help="Create policy related information in CloudPoint")

    """ PRIVILEGE RELATED PARSING """
    parser_privileges = subparser_main.add_parser(
        "privileges", help="Privilege related operations")
    subparser_priviliges = parser_privileges.add_subparsers(
        dest="privileges_command", metavar='<positional argument>')
    # SHOW [GET] PARSING
    parser_priviliges_show = subparser_priviliges.add_parser(
    "show", help="Show privilege related information")
    parser_priviliges_show.add_argument(
    "-i", "--privilege-id", help="Get information on a particular privilege")
    # CREATE [PUT/POST] PARSING

    """ REPLICATION RELATED PARSING """
    parser_replication = subparser_main.add_parser(
        "replication", help="Replication related operations")
    subparser_replication = parser_replication.add_subparsers(
        dest="replication_command", metavar='<positional argument>')
    # SHOW [GET] PARSING
    parser_replication_show = subparser_replication.add_parser(
        "show", help="Show information on replication rules")
    parser_replication_show.add_argument(
        "-i", "--policy-name", help="Get information on a specific replication rule")
    subparser_replication_show = parser_replication_show.add_subparsers(
        dest="replication_show_command", metavar='positional argument>')
    parser_replication_show_rules = subparser_replication_show.add_parser(
        "rules", help="Show replication rules for a policy")
    # CREATE [PUT/POST] PARSING
    parser_replication_create = subparser_replication.add_parser(
        "create", help="Create replication related information in CloudPoint")
    subparser_replication_create = parser_replication_create.add_subparsers(
        dest="replication_create_command", metavar='<positional argument>')
    parser_replication_create_replication_rule = subparser_replication_create.add_parser(
        "replication-rule", help="Create a replication rule")

    """ REPORT RELATED PARSING """
    parser_reports = subparser_main.add_parser(
        "reports", help="Report related operations")
    subparser_reports = parser_reports.add_subparsers(
        dest="reports_command", metavar='<positional argument>')
    # SHOW [GET] PARSING
    parser_reports_show = subparser_reports.add_parser(
        "show", help="Show information on reports")
    parser_reports_show.add_argument(
        "-i", "--report-id", help="Get information on a specific report ID")
    subparser_reports_show = parser_reports_show.add_subparsers(
        dest="reports_show_command", metavar='<positional argument>')
    parser_reports_show_preview = subparser_reports_show.add_parser(
        "preview", help="Show first 10 lines of data for a particular report")
    parser_reports_show_report_data = subparser_reports_show.add_parser(
        "report-data", help="Show data collected by a specific report")
    # CREATE [PUT/POST] PARSING
    parser_reports_create = subparser_reports.add_parser(
        "create", help="Create report related information in CloudPoint")
    # DELETE PARSING
    parser_reports_delete = subparser_reports.add_parser(
        "delete", help="Delete report related information in CloudPoint")
    parser_reports_delete.add_argument(
        "-i", "--report-id", help="Delete data related to a specific REPORT_ID in CloudPoint")
    parser_reports_delete.add_argument(
        "-f", "--full", help="Delete both report data and report in CloudPoint")


    """ ROLE RELATED PARSING """
    parser_roles = subparser_main.add_parser(
        "roles", help="Role related operations")
    subparser_roles = parser_roles.add_subparsers(
        dest="roles_command", metavar='<positional argument>')
    # SHOW [GET] PARSING
    parser_roles_show = subparser_roles.add_parser(
        "show", help="Show role related information")
    parser_roles_show.add_argument(
        "-i", "--role-id", help="Get information on a specific role ID")
    # CREATE [PUT/POST] PARSING
    parser_roles_create = subparser_roles.add_parser(
        "create", help="Create role related information")
    subparser_roles_create = parser_roles_create.add_subparsers(
        dest="roles_create_command", metavar='<positional argument>')
    parser_roles_create_role_assignments = subparser_roles_create.add_parser(
        "role-assignments",
        help="Assign an existing role to an existing user")
    # DELETE PARSING
    parser_roles_delete = subparser_roles.add_parser(
        "delete", help="Delete roles")
    parser_roles_delete.add_argument(
        "-i", "--role-id", help="Delete a specific role within CloudPoint")

    """ TAG RELATED PARSING """
    parser_tags = subparser_main.add_parser(
        "tags", help="Tag related operations")
    subparser_tags = parser_tags.add_subparsers(
        dest="tags_command", metavar='<positional argument>')
    # SHOW [GET] PARSING
    parser_tags_show = subparser_tags.add_parser(
        "show", help="Show Classification tags related information")
    # CREATE [PUT/POST] PARSING
        

    """ TASK RELATED PARSING """
    parser_tasks = subparser_main.add_parser(
        "tasks", help="Task related operations")
    subparser_tasks = parser_tasks.add_subparsers(
        dest="tasks_command", metavar='<positional argument>')
    # SHOW [GET] PARSING
    parser_tasks_show = subparser_tasks.add_parser(
        "show", help="Show information on CloudPoint tasks")
    parser_tasks_show.add_argument(
        "-i", "--task-id", help="Show information on a specific task-id")
    parser_tasks_show.add_argument(
        "-l", "--limit", help="Limit number of results to <LIMIT>")
    parser_tasks_show.add_argument(
        "-r", "--run-since",
        help="Filter on tasks started in last <RUN_SINCE> no. of hours")
    parser_tasks_show.add_argument(
        "-s", "--status", help="Filter on status, valid values for status are :\
        ['running', 'successful', 'failed']", metavar='<STATUS>',
        choices=['running', 'successful', 'failed'])
    parser_tasks_show.add_argument(
        "-t", "--task-type", help="Filter on task type, valid values for task \
        types are : ['create-snapshot', 'create-group-snapshot',\
        'delete-snapshot', 'delete-group-snapshots', 'restore']",
        metavar='TASK_TYPE', choices=['create-snapshot', 'create-group-snapshot',\
        'delete-snapshot', 'delete-group-snapshots', 'restore'])
    subparser_tasks_show = parser_tasks_show.add_subparsers(
        dest="tasks_show_command", metavar='<positional argument>')
    parser_tasks_show_summary = subparser_tasks_show.add_parser(
        "summary", help="Get summary information of all tasks")
    # CREATE [PUT/POST] PARSING
        

    """ TELEMETRY RELATED PARSING """
    parser_telemetry = subparser_main.add_parser(
        "telemetry", help="Telemetry related operations")
    subparser_telemetry = parser_telemetry.add_subparsers(
        dest='telemetry_command', metavar='<positional argument>')
    # SHOW [GET] PARSING
    parser_telemetry_show = subparser_telemetry.add_parser(
        "show", help="Show CloudPoint's Telemetry status [on/off]")
    # CREATE [PUT/POST] PARSING
    parser_telemetry_enable = subparser_telemetry.add_parser(
        "enable", help="Turn ON telemetry for CloudPoint")

    """ USER RELATED PARSING """
    parser_users = subparser_main.add_parser(
        "users", help="User related operations")
    subparser_users = parser_users.add_subparsers(
        dest="users_command", metavar='<positional argument>')
    # SHOW [GET] PARSING
    parser_users_show = subparser_users.add_parser(
        "show", help="Show information on CloudPoint users")
    parser_users_show.add_argument(
        "-i", "--user-id",
        help="Get information on a particular CloudPoint user")
    # CREATE [PUT/POST] PARSING
    parser_users_create = subparser_users.add_parser(
        "create", help="Create user related information in CloudPoint")
    parser_users_create.add_argument(
        "user", help="Create a new user within CloudPoint")
    parser_users_reset_password = subparser_users.add_parser(
        "reset-password", help="Reset a user's password")

    parser_version = subparser_main.add_parser(
        "version", help="Get CloudPoint's current version")

    return parser_main


def run(pass_args=None):
    parser = create_parser()
    args = parser.parse_args(pass_args)
    output = getattr(globals()[args.command], "entry_point")(args)
    return output
    
if __name__ == '__main__':

    parser_main = create_parser()
    argcomplete.autocomplete(parser_main)
    if len(sys.argv) == 1:
        parser_main.print_help()
        sys.exit(-1)
    else:
        #args = parser_main.parse_known_args(sys.argv[1:])
        args = parser_main.parse_args()
        print(args)
        output = getattr(globals()[args.command], "entry_point")(args)
        getattr(globals()[args.command], "pretty_print")(output)
