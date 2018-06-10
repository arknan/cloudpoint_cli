# Global Settings

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
    "replication": "replication/default/rules",
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

METHOD_DICT = {
    "show": "gets",
    "create": "posts",
    "login": "authenticate"
}
EXCEPTION_LIST = []
COMMON_DECIDER_PATHS = ["privileges", "roles", "users", "policies"]
DECIDER_PATHS = ["assets", "agents", "plugins",
                 "licenses", "tasks", "reports", "settings"]

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
