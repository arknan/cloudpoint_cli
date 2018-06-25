#!/usr/bin/env python3

import sys
import json
from getpass import getpass
import constants as co
import cldpt
import api


def role_assignments(args, endpoint):

    """
    data = None
    if co.check_attr(args, 'file_name'):
        file_name = getattr(args, 'file_name')
        with open(file_name, 'r') as file_handle:
            try:
                data = json.load(file_handle)
            except json.decoder.JSONDecodeError:
                print("{} isn't JSON formatted, refer to the admin guide for \
formatting details.".format(file_name))
                sys.exit(-22)
    else:
    """

    print("\nPlease choose a name that you want this role to be called")
    role_name = input("Role name : ")
    roles = json.loads(cldpt.run(["show", "privileges"]))
    roles_list = []
    for row in roles:
        roles_list.append(row["name"])
    print("\nPlease choose a role type, valid role types include : ",
          roles_list)
    role_type = str(input("Role type to associate: "))
    if role_type not in co.VALID_PRIVILEGES:
        print("\nThat is not a valid role type !\n")
        sys.exit(-23)
    print("\nEnter the user's email address that should be associated \
with this role")
    user_email = str(input("Email Address : "))
    data = {
        "name": role_name,
        "privileges": [{
            "name": role_type
        }],
        "subjects": [{
            "name": user_email
        }]
    }

    return (data, endpoint)


def email_config(args, endpoint):

    # This doesn't seem to work currently,
    # maybe the data format is wrong ! need to check with ENGG
    print("\nPlease enter the IP address of SMTP server")
    smtp_ip = input("IP Address : ")
    print("\nPlease enter the port used by SMTP")
    smtp_port = input("Port (25) : ")
    if not smtp_port:
        smtp_port = 25
    print("\nPlease enter SMTP credentials [skip if anonymous authentication]")
    smtp_user = input("User name : ")
    smtp_passwd = None
    auth = False
    if smtp_user:
        auth = True
        smtp_passwd = getpass("Password: ")
    print("\nPlease enter the smtp sender email address")
    smtp_email = input("Sender Email : ")

    data = {
        "type": "smtp",
        "senderEmail": smtp_email,
        "data": {
            "host": smtp_ip,
            "port": smtp_port,
            "authentication": "false"
        }
    }
    if auth:
        data["data"]["username"] = smtp_user
        data["data"]["password"] = smtp_passwd
        data["data"]["authentication"] = "true"

    return (data, endpoint)


def user(args, endpoint):

    print("\nPlease note that users must be accessible by both ", end='')
    print("LDAP[Name] and SMTP[email address]")
    first_name = input("Firstname : ")
    last_name = input("Lastname : ")
    email_addr = input("Email : ")

    data = {
        "lastName": last_name,
        "email": email_addr,
        "firstName": first_name
    }

    return (data, endpoint)


def snapshots(args, endpoint):

    if co.check_attr(args, "asset_id"):
        endpoint.append('/assets/')
        endpoint.append(args.asset_id)
        endpoint.append('/snapshots/')
    else:
        print("\nPlease mention an ASSET_ID for taking snapshot\n")
        sys.exit(-1)

    snap_types = json.loads(cldpt.run(
        ["show", "assets", "-i", args.asset_id]))["snapMethods"]
    print("\nPlease enter a snapshot type")
    print("Valid types for this asset include :", snap_types)
    snap_type = input("SnapType : ")
    snap_name = input("Snapshot Name : ")
    snap_descr = input("Description : ")
    snap_bool = None
    while True:
        snap_bool = input("Consistent ? [True / False] : ")
        if snap_bool in ["True", "False"]:
            break
        else:
            print("\nChoose either 'True' or 'False'\n")
    data = {
        "snapType": snap_type,
        "name": snap_name,
        "description": snap_descr,
        "consistent": snap_bool
    }

    return (data, endpoint)


def replicas(args, endpoint):

    print("\nEnter the snapshot ID to replicate and the destination(s)\n")
    print("A maximum of 3 destinations are allowed\n")
    snap_id = input("Snapshot ID : ")

    snap_info = json.loads(getattr(api.Command(), 'gets')(
        '/assets/' + snap_id))
    snap_source_asset = snap_info["snapSourceId"]
    repl_locations = json.loads(getattr(api.Command(), 'gets')(
        '/assets/' + snap_source_asset + '/snapshots/' + snap_id +
        '/repl-targets/'))

    valid_locations = []
    for i in repl_locations:
        valid_locations.append(i["region"])

    print("Enter destination region(s) as comma separated values.")
    print("Valid destination regions are : {}".format(valid_locations))

    dest_counter = 0
    dest = []
    while dest_counter < 3:
        temp = input("Destination : (enter 'none' if you are done) ")
        if temp == 'none':
            break

        elif temp in valid_locations:
            for i in repl_locations:
                if temp == i["region"]:
                    dest.append(i["id"])
                    dest_counter += 1

        else:
            print("\nNot a valid location\n")
            print("Valid destination regions are : {}".format(valid_locations))

    if not dest:
        print("\nYou should provide atleast 1 region to replicate to !\n")
        sys.exit(-1)

    data = {
        "snapType": "replica",
        "srcSnapId": snap_id,
        "dest": dest
    }
    endpoint.append('/assets/')
    endpoint.append(snap_source_asset)
    endpoint.append('/snapshots/')

    return (data, endpoint)


def restore(args, endpoint):
    if co.check_attr(args, "snap_id"):
        endpoint.append("/" + args.snap_id)
    else:
        print("\nPlease mention a SNAP_ID for doing restores\n")
        sys.exit(-1)

    print("\nPlease enter a restore location.\n")
    print("Valid values are [new, original]\n")
    restore_loc = None
    data = {
        "snapid": args.snap_id
    }
    while True:
        restore_loc = input("Restore Location : ")
        if restore_loc in ['new', 'original']:
            break
    if restore_loc == 'new':
        snap_info = json.loads(getattr(api.Command(), 'gets')(
            '/assets/' + args.snap_id))
        snap_source_id = snap_info["snapSourceId"]
        snap_type = snap_info["attachment"]["type"]
        if snap_type == 'host':
            data["dest"] = snap_source_id
        else:
            print("\nSnapshot type is : ", snap_type)
            print("\nOnly host type snapshots are supported thru CLI\n")
    else:
        pass

    return (data, endpoint)


def policies(args, endpoint):

    """

    name, appConsist, tag, snapTypePref, hour = None, None, None, None, None
    schedule = {}
    print(name, appConsist, tag, snapTypePref, hour, schedule)

    while True:
        name = input("Policy Name : ")
        if (len(name) > 32) or (len(name) < 2):
            print("Policy Name should be between 2 and 32 characters\n")
        else:
            break

    while True:
        appConsist = input("Application Consistent ['True' or 'False'] : ")
        if appConsist not in ['True', 'False']:
            print("\nValid options are 'True' or 'False'\n")
        else:
            if appConsist == 'True':
                appConsist = True
                break
            else:
                appConsist = False
                break

    tag = input("Description of Policy : ")
    while True:
        snapTypePref = input("Snapshot type ['cow', 'clone'] : ")
        if snapTypePref not in ['cow', 'clone']:
            print("\nValid options are 'cow' or 'clone'\n")
        else:
            break

    sched_dict = {
        'minute': 'Backup every __ minute(s) :',
        'hour' : 'Backup every __ hour(s) :',
        'day': 'Backup on __day :',



    print("Schedule frequency options, Leave Blank if not applicable :\n")
    freq = input(
        "Backup every \n['minute', 'hour', 'day', 'week', 'month', 'year']\n
        Frequency : ")
    minute = input("Minute : ") or "0"
    hour = input("Hour : ") or "0"
    mday = input("Date : ") or "1"
    month = input("Month : ") or "1"
    wday = input("Day of the week : ")
    mday = input("Date of the month: ")


    """
    pass


def replication_rule(args, endpoint):

    repl_locations = json.loads(getattr(api.Command(), 'gets')(
        '/replica-locations/'))
    valid_sources = {x['region']: x['id'] for x in repl_locations}
    source = None
    while True:
        print("Enter a source region, valid values are:\n{}".format(
            list(valid_sources.keys())))
        source_region = input("Source region : ")
        if source_region in valid_sources:
            source = (valid_sources[source_region])
            del valid_sources[source_region]
            break
        else:
            print("Not a valid choice, please try again\n")

    dest_counter = 0
    dest = []
    while dest_counter < 3:
        temp = input("Destination : (enter 'none' if you are done) ")
        if temp == 'none':
            break

        elif temp in valid_sources:
            dest.append(valid_sources[temp])
            dest_counter += 1

        else:
            print("\nNot a valid location\n")
            print("Valid destination regions are : {}".format(
                list(valid_sources.keys())))

    if not dest:
        print("\nYou should provide atleast 1 region to replicate to !\n")
        sys.exit(-1)

    data = {
        "destination": dest,
        "source": source
    }

    return (data, endpoint)


def reports(args, endpoint):


    """
    report_id = input("Report Name : ")

    first_name = input("Firstname : ")
    last_name = input("Lastname : ")
    email_addr = input("Email : ")

    data = {
        "lastName": last_name,
        "email": email_addr,
        "firstName": first_name
    }

    return (data, endpoint)
    """
    print("Not implemented\n")
    sys.exit(-1)
