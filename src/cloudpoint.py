#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import configparser
import sys
import argparse
import argcomplete

import agents
import assets
import authenticate
import email_config
import ldap_config
import licenses
import logs
import plugins
import policies
import privileges
import replication
import reports
import roles
import tags
import tasks
import telemetry
import users
import version

LOG_F = logs.setup(__name__, 'f')
LOG_FC = logs.setup(__name__)


def create_parser():

    """ MAIN PARSER """
    parser_main = argparse.ArgumentParser()
    subparser_main = parser_main.add_subparsers(
        dest='command', metavar='<positional argument>')

    """ AGENT RELATED PARSING """
    parser_agents = subparser_main.add_parser(
        "agents", help="Agent related operations")
    subparser_agents = parser_agents.add_subparsers(
        dest="agents_command", metavar='<positional argument>')
    # DELETE PARSING
    parser_agents_delete = subparser_agents.add_parser(
        "delete", help="Delete agent related information in CloudPoint")
    subparser_agents_delete = parser_agents_delete.add_subparsers(
        dest="agents_delete_command", metavar='<positional argument>')
    parser_agents_delete_agent = subparser_agents_delete.add_parser(
        "agent", help="Delete agent")
    parser_agents_delete_agent.add_argument(
        "-i", "--agent-id", help="Delete a specific agent", required=True)
    subparser_agents_delete_agent = parser_agents_delete_agent.add_subparsers(
        dest="agents_delete_agent_command", metavar='<positional argument>')
    parser_agents_delete_agent_plugins = \
        subparser_agents_delete_agent.add_parser(
            "plugins", help="Delete plugins of a specific agent")
    parser_agents_delete_agent_plugins.add_argument(
        "-i", "--plugin-name", required=True,
        help="Delete a specific plugin for a specific agent")
    subparser_agents_delete_agent_plugins =\
        parser_agents_delete_agent_plugins.add_subparsers(
            dest="agents_delete_agent_plugins_command",
            metavar='<positional argument>')
    parser_agents_delete_agent_plugins_config =\
        subparser_agents_delete_agent_plugins.add_parser(
            "config", help="Delete plugin configuration")
    parser_agents_delete_agent_plugins_config.add_argument(
        "-i", "--config-id", required=True,
        help="Delete a specific configuration of a plugin")
    # SHOW [GET] PARSING
    parser_agents_show = subparser_agents.add_parser(
        "show", help="Show agent related information")
    parser_agents_show.add_argument(
        "-i", "--agent-id",
        help="Show information related to a specific agent")
    subparser_agents_show = parser_agents_show.add_subparsers(
        dest="agents_show_command", metavar='<positional argument>')
    parser_agents_show_plugins = subparser_agents_show.add_parser(
        "plugins", help="Show related plugins for an agent")
    parser_agents_show_plugins.add_argument(
        "-i", "--plugin-name", dest="configured_plugin_name",
        help="Show plugin information for a specific agent plugin")
    parser_agents_show_summary = subparser_agents_show.add_parser(
        "summary", help="Show summary of agents")
    subparser_agents_show_plugins = parser_agents_show_plugins.add_subparsers(
        dest="agents_show_plugins_command", metavar='<positional argument>')
    parser_agents_show_plugins_configs =\
        subparser_agents_show_plugins.add_parser(
            "configs", help="Show configuration of a specific plug-in")

    """ ASSET RELATED PARSING """
    parser_assets = subparser_main.add_parser(
        "assets", help="Asset releated operations")
    subparser_assets = parser_assets.add_subparsers(
        dest="assets_command", metavar='<positional argument>')

    # CREATE [PUT/POST] PARSING
    parser_assets_create_snapshot = subparser_assets.add_parser(
        "create-snapshot", help="Take snapshots of assets")
    parser_assets_create_snapshot.add_argument(
        "-i", "--asset-id", help="Provide an ASSET_ID to snap")
    # DELETE PARSING
    parser_assets_delete_snapshot = subparser_assets.add_parser(
        "delete-snapshot", help="Delete snapshots")
    parser_assets_delete_snapshot.add_argument(
        "-i", "--snapshot-id", help="Delete a specific snapshot_id")
    parser_assets_delete_snapshot.add_argument(
        "-f", "--file-name", help="File containing snapshot_ids to be deleted")
    # CREATE [PUT/POST] PARSING - ROUND 2 
    parser_assets_policy = subparser_assets.add_parser(
        "policy", help="Assign/Remove a policy to/from an asset")
    parser_assets_policy.add_argument(
        "-i", "--asset-id", required=True,
        help="Provide an ASSET_ID to assign a policy to")
    subparser_assets_policy = parser_assets_policy.add_subparsers(
        dest="assets_policy_command", metavar='<positional argument>')
    parser_assets_policy_assign = subparser_assets_policy.add_parser(
        "assign", help="Assign a policy to an asset")
    parser_assets_policy_assign.add_argument(
        "-i", "--policy-id", required=True,
        help="Provide a policy_id to assign to an asset")
    parser_assets_policy_remove = subparser_assets_policy.add_parser(
        "remove", help="Remove a policy from an asset")
    parser_assets_policy_remove.add_argument(
        "-i", "--policy-id", required=True,
        help="Provide a policy_id to remove from an asset")
    parser_assets_replicate = subparser_assets.add_parser(
        "replicate", help="Replicate Existing snapshots")
    parser_assets_replicate.add_argument(
        "-i", "--snapshot-id", help="Provide a SNAPSHOT_ID to replicate")

    parser_assets_restore = subparser_assets.add_parser(
        "restore", help="Restore snapshots")
    parser_assets_restore.add_argument(
        "-i", "--snapshot-id", help="Provide a SNAPSHOT_ID to restore")
    # SHOW [GET] PARSING
    parser_assets_show = subparser_assets.add_parser(
        "show", help="Show assets related information")
    parser_assets_show.add_argument(
        "-i", "--asset-id",
        help="Show information related to a specific asset")
    subparser_assets_show = parser_assets_show.add_subparsers(
        dest="assets_show_command", metavar='<positional argument>')
    parser_assets_show_policies = subparser_assets_show.add_parser(
        "policies", help="Show policies associated with an asset")
    parser_assets_show_snapshots = subparser_assets_show.add_parser(
        "snapshots", help="Show related snapshots for an asset")
    parser_assets_show_snapshots.add_argument(
        "-i", "--snapshot-id",
        help="Show snapshot information for a specific snapshot")
    subparser_assets_show_snapshots = \
        parser_assets_show_snapshots.add_subparsers(
            dest="snapshots_command", metavar='<positional argument>')
    parser_assets_show_snapshots_granules = \
        subparser_assets_show_snapshots.add_parser(
            "granules", help="Show granules for a snapshot of an asset")
    parser_assets_show_snapshots_granules.add_argument(
        "-i", "--granule-id", help="Show information on a particular granule")
    parser_assets_show_snapshots_restore_targets = \
        subparser_assets_show_snapshots.add_parser(
            "restore-targets",
            help="Show restore target locations for a specific snapshot asset")
    parser_assets_show_summary = subparser_assets_show.add_parser(
        "summary", help="Show summary of assets")

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
    parser_email_config_create_aws_ses = \
        subparser_email_config_create.add_parser(
            "aws_ses", help="Add AWS SES Email configuration")
    parser_email_config_create_send_grid = \
        subparser_email_config_create.add_parser(
            "send_grid", help="Add SendGrid Email configuration")
    parser_email_config_create_smtp = \
        subparser_email_config_create.add_parser(
            "smtp", help="Add SMTP Email configuration")
    # DELETE RELATED PARSING
    parser_email_config_delete = subparser_email_config.add_parser(
        "delete", help="Delete email configuration from CloudPoint")

    """ LDAP RELATED PARSING """
    parser_ldap_config = subparser_main.add_parser(
        "ldap_config", help="LDAP related operations")
    subparser_ldap_config = parser_ldap_config.add_subparsers(
        dest="ldap_config_command", metavar='<positional argument>')
    # SHOW [GET] PARSING
    parser_ldap_config_show = subparser_ldap_config.add_parser(
        "show", help="Show LDAP related details")

    """ LICENSE RELATED PARSING """
    parser_licenses = subparser_main.add_parser(
        "licenses", help="Licensing related operations")
    subparser_licenses = parser_licenses.add_subparsers(
        dest="licenses_command", metavar='<positional argument>')
    # CREATE [PUT/POST] PARSING
    parser_licenses_add = subparser_licenses.add_parser(
        "add", help="Add a license to CloudPoint")
    parser_licenses_add.add_argument(
        "-f", "--file-name", required=True,
        help="Provide the full path to the license file (.slf)")
    # DELETE PARSING
    parser_licenses_delete = subparser_licenses.add_parser(
        "delete", help="Delete a license from CloudPoint")
    parser_licenses_delete.add_argument(
        "-i", "--license-id", help="Delete a specific license", required=True)
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
        "description",
        help="Get plugin description for a specific plugin name")
    parser_plugins_show_summary = subparser_plugins_show.add_parser(
        "summary", help="Show summary information for plugins")

    """ POLICY RELATED PARSING """
    parser_policies = subparser_main.add_parser(
        "policies", help="Policy related operations")
    subparser_policies = parser_policies.add_subparsers(
        dest="policies_command", metavar='<positional argument>')
    # ADD/REMOVE ASSETS [PATCH] PARSING
    parser_policies_asset = subparser_policies.add_parser(
        "asset", help="Add/Remove assets to policies")
    parser_policies_asset.add_argument(
        "-i", "--policy-id", help="policy_id to add/remove asset to/from")
    parser_policies_asset.add_argument(
        "-n", "--policy-name", help="policy_name to add/remove asset to/from")
    subparser_policies_asset = parser_policies_asset.add_subparsers(
        dest="policies_asset_command", metavar='<positional argument>')
    parser_policies_asset_add = subparser_policies_asset.add_parser(
        "add", help="Add asset(s) to a policy")
    parser_policies_asset_add.add_argument(
        "-i", "--asset-id", help="Asset_id to add to the policy")
    parser_policies_asset_add.add_argument(
        "-f", "--file-name", help="File containing assets to be added")
    parser_policies_asset_remove = subparser_policies_asset.add_parser(
        "remove", help="Remove asset(s) from a policy")
    parser_policies_asset_remove.add_argument(
        "-i", "--asset-id", help="Asset_id to remove from the policy")
    parser_policies_asset_remove.add_argument(
        "-f", "--file-name", help="File containing assets to be removed")
    # CREATE [PUT/POST] PARSING
    parser_policies_create = subparser_policies.add_parser(
        "create", help="Create policy related information in CloudPoint")
    # DELETE PARSING
    parser_policies_delete = subparser_policies.add_parser(
        "delete", help="Delete a policy from CloudPoint")
    parser_policies_delete.add_argument(
        "-i", "--policy-id", help="policy_id to delete")
    parser_policies_delete.add_argument(
        "-n", "--policy-name", help="policy_name to delete")
    # SHOW [GET] PARSING
    parser_policies_show = subparser_policies.add_parser(
        "show", help="Show policy related information")
    parser_policies_show.add_argument(
        "-i", "--policy-id", help="Show information on a particular policy id")
    parser_policies_show.add_argument(
        "-n", "--policy-name",
        help="Show information on a particular policy name")
    subparser_policies_show = parser_policies_show.add_subparsers(
        dest="policies_show_command", metavar='<positional argument>')
    parser_policies_show_protected_assets = subparser_policies_show.add_parser(
        "protected-assets",
        help="Show all protected assets and policies protecting them")
    subparser_policies_show_protected_assets = \
        parser_policies_show_protected_assets.add_subparsers(
            dest="policies_show_protected_assets_command",
            metavar='<positional argument>')
    parser_policies_show_protected_assets_assets_only = \
        subparser_policies_show_protected_assets.add_parser(
            "assets-only",
            help="Show a list of protected assets, not their policy")
    parser_policies_show_unprotected_assets = subparser_policies_show.add_parser(
        "unprotected-assets", help="Show all unprotected assets")

    """ PRIVILEGE RELATED PARSING """
    parser_privileges = subparser_main.add_parser(
        "privileges", help="Privilege related operations")
    subparser_priviliges = parser_privileges.add_subparsers(
        dest="privileges_command", metavar='<positional argument>')
    # SHOW [GET] PARSING
    parser_priviliges_show = subparser_priviliges.add_parser(
        "show", help="Show privilege related information")
    parser_priviliges_show.add_argument(
        "-i", "--privilege-id",
        help="Get information on a particular privilege")

    """ REPLICATION RELATED PARSING """
    parser_replication = subparser_main.add_parser(
        "replication", help="Replication related operations")
    subparser_replication = parser_replication.add_subparsers(
        dest="replication_command", metavar='<positional argument>')
    # CREATE [PUT/POST] PARSING
    parser_replication_create = subparser_replication.add_parser(
        "create", help="Create replication related information in CloudPoint")
    subparser_replication_create = parser_replication_create.add_subparsers(
        dest="replication_create_command", metavar='<positional argument>')
    parser_replication_create_replication_rule = \
        subparser_replication_create.add_parser(
            "replication_rule", help="Create a replication rule")
    # DELETE PARSING
    parser_replication_delete = subparser_replication.add_parser(
        "delete", help="Delete replication related information")
    subparser_replication_delete = parser_replication_delete.add_subparsers(
        dest="replication_delete_command", metavar='<positional argument>')
    parser_replication_delete_replication_rule = \
        subparser_replication_delete.add_parser(
            "replication_rule", help="Delete a replication rule")
    # MODIFY PARSING
    parser_replication_modify = subparser_replication.add_parser(
        "modify", help="Modify replication related information")
    subparser_replication_modify = parser_replication_modify.add_subparsers(
        dest="replication_modify_command", metavar='<positional argument>')
    parser_replication_modify_replication_rule = \
        subparser_replication_modify.add_parser(
            "replication_rule", help="Modify a replication rule")
    # SHOW [GET] PARSING
    parser_replication_show = subparser_replication.add_parser(
        "show", help="Show information on replication rules")
    parser_replication_show.add_argument(
        "-i", "--policy-name",
        help="Get information on a specific replication rule")
    subparser_replication_show = parser_replication_show.add_subparsers(
        dest="replication_show_command", metavar='positional argument>')
    parser_replication_show_rules = subparser_replication_show.add_parser(
        "rules", help="Show replication rules for a policy")

    """ REPORT RELATED PARSING """
    parser_reports = subparser_main.add_parser(
        "reports", help="Report related operations")
    subparser_reports = parser_reports.add_subparsers(
        dest="reports_command", metavar='<positional argument>')
    # CREATE [POST] PARSING
    parser_reports_create = subparser_reports.add_parser(
        "create", help="Create report related information in CloudPoint")
    # DELETE PARSING
    parser_reports_delete = subparser_reports.add_parser(
        "delete", help="Delete report related information in CloudPoint")
    parser_reports_delete.add_argument(
        "-i", "--report-id",
        help="Delete ONLY DATA related to a specific REPORT_ID in CloudPoint")
    subparser_reports_delete = parser_reports_delete.add_subparsers(
        dest="reports_delete_command", metavar='<positional argument>')
    parser_reports_delete_full = subparser_reports_delete.add_parser(
        "full", help="Delete both report data and report in CloudPoint")
    # RE_RUN [PUT] PARSING
    parser_reports_re_run = subparser_reports.add_parser(
        "re_run", help="Re-Run an existing report in CloudPoint")
    parser_reports_re_run.add_argument(
        "-i", "--report-id", help="Re-Run a specific REPORT_ID in CloudPoint")
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
    parser_reports_show_report_types = subparser_reports_show.add_parser(
        "report-types", help="Show available report types")

    """ ROLE RELATED PARSING """
    parser_roles = subparser_main.add_parser(
        "roles", help="Role related operations")
    subparser_roles = parser_roles.add_subparsers(
        dest="roles_command", metavar='<positional argument>')
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
    # MODIFY PARSING
    parser_roles_modify = subparser_roles.add_parser(
        "modify", help="Modify roles")
    # SHOW [GET] PARSING
    parser_roles_show = subparser_roles.add_parser(
        "show", help="Show role related information")
    parser_roles_show.add_argument(
        "-i", "--role-id", help="Get information on a specific role ID")

    """ TAG RELATED PARSING """
    parser_tags = subparser_main.add_parser(
        "tags", help="Classification tag related operations")
    subparser_tags = parser_tags.add_subparsers(
        dest="tags_command", metavar='<positional argument>')
    # SHOW [GET] PARSING
    parser_tags_show = subparser_tags.add_parser(
        "show", help="Show Classification tags related information")

    """ TASK RELATED PARSING """
    parser_tasks = subparser_main.add_parser(
        "tasks", help="Task related operations")
    subparser_tasks = parser_tasks.add_subparsers(
        dest="tasks_command", metavar='<positional argument>')
    # DELETE PARSING
    parser_tasks_delete = subparser_tasks.add_parser(
        "delete", help="Delete a task from CloudPoint")
    parser_tasks_delete.add_argument(
        "-i", "--task-id", help="Delete a specific task id")
    parser_tasks_delete.add_argument(
        "-s", "--status", help="Delete ALL tasks with a specified status,\
        Valid values are : ['running', 'successful', 'failed']",
        choices=['running', 'successful', 'failed'], metavar='<STATUS>')
    parser_tasks_delete.add_argument(
        "-o", "--older-than", metavar='<OLDER_THAN>',
        help="Delete ALL tasks older than <OLDER_THAN> days")
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
        "-s", "--status", metavar='<STATUS>',
        help="Filter on status, valid values for status are :\
        ['running', 'successful', 'failed']",
        choices=['running', 'successful', 'failed'])
    parser_tasks_show.add_argument(
        "-t", "--task-type", help="Filter on task type, valid values for task \
        types are : ['create-snapshot', 'create-group-snapshot',\
        'delete-snapshot', 'delete-group-snapshots', 'restore']",
        metavar='TASK_TYPE', choices=[
            'create-snapshot', 'create-group-snapshot', 'delete-snapshot',
            'delete-group-snapshots', 'restore'])
    subparser_tasks_show = parser_tasks_show.add_subparsers(
        dest="tasks_show_command", metavar='<positional argument>')
    parser_tasks_show_summary = subparser_tasks_show.add_parser(
        "summary", help="Get summary information of all tasks")

    """ TELEMETRY RELATED PARSING """
    parser_telemetry = subparser_main.add_parser(
        "telemetry", help="Telemetry related operations")
    subparser_telemetry = parser_telemetry.add_subparsers(
        dest='telemetry_command', metavar='<positional argument>')
    # CREATE [PUT/POST] PARSING
    parser_telemetry_enable = subparser_telemetry.add_parser(
        "enable", help="Turn ON telemetry for CloudPoint")
    # DELETE PARSING
    parser_telemetry_disable = subparser_telemetry.add_parser(
        "disable", help="Turn OFF telemetry for CloudPoint")
    # SHOW [GET] PARSING
    parser_telemetry_status = subparser_telemetry.add_parser(
        "status", help="Show CloudPoint's Telemetry status [on/off]")

    """ USER RELATED PARSING """
    parser_users = subparser_main.add_parser(
        "users", help="User related operations")
    subparser_users = parser_users.add_subparsers(
        dest="users_command", metavar='<positional argument>')
    # CREATE [PUT/POST] PARSING
    parser_users_create = subparser_users.add_parser(
        "create", help="Create user related information in CloudPoint")
    parser_users_create.add_argument(
        "user", help="Create a new user within CloudPoint")
    parser_users_reset_password = subparser_users.add_parser(
        "reset_password", help="Reset a user's password")
    # SHOW [GET] PARSING
    parser_users_show = subparser_users.add_parser(
        "show", help="Show information on CloudPoint users")
    parser_users_show.add_argument(
        "-i", "--user-id",
        help="Get information on a particular CloudPoint user")

    """ VERSION RELATED PARSING """
    parser_version = subparser_main.add_parser(
        "version", help="Get CloudPoint's current version")

    return parser_main


def run(pass_args=None):
    LOG_F.debug("cloudpoint.run called with %s", pass_args)
    parser = create_parser()
    args = parser.parse_args(pass_args)
    output = getattr(globals()[args.command], "entry_point")(args)
    return output


if __name__ == '__main__':

    config = configparser.ConfigParser()
    if not config.read('/root/.cloudpoint_cli.config'):
        LOG_FC.error("cloudpoint_cli.config is empty or missing\n")
        sys.exit(1)

    parser_main = create_parser()
    argcomplete.autocomplete(parser_main)
    if len(sys.argv) == 1:
        parser_main.print_help()
        sys.exit(1)
    else:
        args = parser_main.parse_args()
        LOG_F.debug("Calling %s.entry_point() with %s", args.command, args)
        output = getattr(globals()[args.command], "entry_point")(args)
        LOG_F.debug("From %s.entry_point() Received :\n%s",
                    args.command, output)
        getattr(globals()[args.command], "pretty_print")(args, output)
