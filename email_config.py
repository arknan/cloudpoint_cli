#!/usr/bin/env python3

def settings(endpoint, args):

    if co.check_attr(args, 'settings_command'):
        if getattr(args, 'settings_command') == "ad":
            endpoint.append("idm/config/ad")
        elif getattr(args, 'settings_command') == "smtp":
            endpoint.append("email/config")

    return endpoint
