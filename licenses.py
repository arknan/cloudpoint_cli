#!/usr/bin/env python3

def licenses(endpoint, args):

    if co.check_attr(args, 'licenses_command'):
        if args.licenses_command == "active":
            endpoint.append('/?IsLicenseActive=true')
        elif args.licenses_command == "features":
            endpoint.append('/all/features')

    if co.check_attr(args, 'license_id'):
        endpoint.append(getattr(args, 'license_id'))

    return endpoint

