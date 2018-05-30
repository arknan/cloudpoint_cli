#!/usr/bin/env python3


import argparse
import api

def main() :
    parser = argparse.ArgumentParser()

#By default action="store" and type="string"
    parser.add_argument("-g", "--get", action="store_true", help="Get information on some attribute")
    parser.add_argument("-a", "--authenticate", action="store_true", help="Login to CloudPoint ; Required for doing any other operation")
    parser.add_argument("-c", "--create", action="store_true", help="Create any information within CloudPoint")

    args = parser.parse_args()
    interface(args)

def interface(args) :
    x = api.Command()
    if args.get :
        x.gets()
    elif  args.create :
        x.posts()
    elif  args.authenticate :
        x.authenticate()
    else :
        print("Invalid Option")

if __name__ == "__main__" :
    main()
