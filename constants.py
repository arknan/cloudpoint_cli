# Global Settings

"""
This module hosts all the global constants that are used in every other module
"""

import os

ROWS, COLUMNS = os.popen('stty size', 'r').read().split()
COLUMNS = int(COLUMNS)

def check_attr(args, attr):

    try:
        if hasattr(args, attr):
            if getattr(args, attr):
                return True
    except NameError:
        return False
    else:
        return False


GETS_DICT = {
    "ad": "idm/config/ad",
    "agents": "agents/",
    "assets": "assets/",
    "tags": "classifications/tags",
    "smtp": "email/config",
    "granules": "granules",
    # "join-tokens": "jointokens/",
    "licenses": "licenses/",
    "plugins": "plugins/",
    "policies": "policies/",
    "privileges": "/authorization/privilege/",
    "replication": "replication/",
    "report-types": "report-types/",
    "reports": "reports/",
    "roles": "authorization/role",
    "schedules": "schedules/",
    "settings": "/",
    "tasks": "tasks/",
    "telemetry": "telemetry/",
    "users": "idm/user/",
    "version": "version"
}

POST_DICT = {
    "role_assignments": "/authorization/role",
    "user": "/idm/user",
    "policies": "/policies/",
    # PUTS DICT
    "email_config": "/email/config",
    "reset_password": "/idm/user/forgotPassword"
}

METHOD_DICT = {
    "show": "gets",
    "create": "posts",
    "authenticate": "authenticate",
    "modify": "puts"
}
PUTS_LIST = ["email_config", "reset_password"]
COMMON_DECIDER_PATHS = ["privileges", "roles", "users", "policies"]
DECIDER_PATHS = ["assets", "agents", "plugins", "replication",
                 "licenses", "tasks", "reports", "settings"]
DONT_PRINT = ['_links', 'links']

EXIT_1 = "\nERROR : Argument 'snapshots' requires -i flag for 'ASSET_ID'\n\
Expected Command Format : cldpt show assets -i <ASSET_ID> snapshots\n"

EXIT_2 = "\nERROR : Granules can only be listed for asset snapshots\n\
Please enter a valid 'SNAP_ID' and 'ASSET_ID'\nExpected Command Format : \
cldpt show assets -i <ASSET_ID> snapshots -i <SNAP_ID> granules\n"

EXIT_3 = "\nERROR : Unknown option passed\n"

EXIT_4 = "\nERROR : You need to provide an argument to SHOW\n\
Expected Command Format : cldpt show assets ; cldpt show reports\n"

EXIT_5 = "\nERROR : Argument 'plugins' requires -i flag for 'AGENT_ID'\n\
Expected Command Format : cldpt show agents -i <AGENT_ID> plugins\n"

EXIT_6 = "\nERROR:Argument 'description' requires -i flag for 'PLUGIN_NAME'\n\
Expected Command Format : cldpt show plugins -i <PLUGIN_NAME> description\n"


VALID_PRIVILEGES = ["REPLICATION_POLICY_MANAGEMENT", "REPORT_MANAGEMENT",
                    "SNAPSHOT_POLICY_MANAGEMENT", "ROLE_MANAGEMENT",
                    "CLASSIFICATION_POLICY_MANAGEMENT", "USER_MANAGEMENT",
                    "CLOUD_AND_ARRAY_MANAGEMENT", "ADMINISTRATOR"]
