#!/usr/bin/env python3

from getpass import getpass


def reset_password():
    # API endpoint is messed up .. this doesn't work either :(
    email_addr = input("Email : ")
    new_passwd = getpass("New Password : ")

    data = {
        "email": email_addr,
        "newPassword": new_passwd
    }

    return data
