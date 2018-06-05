#!/usr/bin/env python3


def check_attr(args, attr):
    try:
        if hasattr(args, attr):
            if getattr(args, attr):
                return True
    except NameError:
        return False
    else:
        return False


def common_paths(endpoint, args):

    detail = (args.sub_command)[:-1] + '_id'
    if check_attr(args, detail):
        endpoint.append(getattr(args, detail))
	
    return endpoint
		
def assets(endpoint, args):
    if check_attr(args, 'asset_id'):
        endpoint.append(args.asset_id)
    if (check_attr(args, 'asset_command')) and\
        (args.asset_command == "snapshots"):
        if check_attr(args, 'asset_id'):
            endpoint.append(args.asset_command)
            if check_attr(args, 'snap_id'):
                endpoint.append(args.snap_id)
        else:
            print(EXIT_1)
            sys.exit(2)

        if (check_attr(args, 'snapshot_command')) and\
           (args.snapshot_command == "granules"):
            if (check_attr(args, 'asset_id')) and\
               (check_attr(args, 'snap_id')):
                endpoint.append(args.snapshot_command + '/')
                if check_attr(args, 'granule_id'):
                    endpoint.append(args.granule_id)
            else:
                print(EXIT_2)
                sys.exit(3)

    return endpoint

def agents(endpoint, args):

    
    detail = (args.sub_command)[:-1] + '_id'
    if check_attr(args, detail):
        endpoint.append(getattr(args, detail))
	
    if (check_attr(args, 'agent_command')) and \
       (args.agent_command == "plugins"):
        if check_attr(args, detail):
            endpoint.append("plugins/")
        else :
            print(EXIT_5)
            sys.exit(101)
        if check_attr(args, "plugin_name"):
            endpoint.append(args.plugin_name)

    return endpoint 
