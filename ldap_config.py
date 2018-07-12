#!/usr/bin/env python3

def entry_point(args):
    if co.check_attr(args, 'settings_command'):
        if getattr(args, 'settings_command') == "ad":
            endpoint.append("idm/config/ad")
