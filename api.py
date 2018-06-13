#!/usr/bin/env python3


import json
import sys
import getpass
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Command():

    def __init__(self):

        self.endpoint = ''
        self.ip_addr = '127.0.0.1'
        self.base_url = 'https://' + self.ip_addr + ':/cloudpoint/api/v2'
        self.verify = False
        self.token_header = None
        self.token_endpoint = None
        self.data = None

        try:
            with open("/root/.cldpt_token", "r") as file_handle:
                self.token = file_handle.readline()
        except FileNotFoundError:
            self.token = None

        self.header = {'Content-Type': 'application/json',
                       'Authorization': 'Bearer {0}'.format(self.token)}

    def authenticate(self):

        self.token_header = {'Content-Type': 'application/json'}
        self.token_endpoint = self.base_url + '/idm/login'
        username = input("Username: ")
        passwd = getpass.getpass("Password: ")
        self.data = json.dumps({
            "email": username,
            "password": passwd})

        response = requests.post(self.token_endpoint, verify=self.verify,
                                 headers=self.token_header, data=self.data)
        if response.status_code == 200:
            self.token = (
                (json.loads(response.content.decode('utf-8')))["accessToken"])

            with open("/root/.cldpt_token", "w") as file_handle:
                file_handle.write(self.token)

        else:
            print(
                (json.loads(response.content.decode('utf-8'))["errorMessage"]))

    def gets(self, endpoint):
        self.endpoint = endpoint
        print(endpoint)
        if not self.token:
            print("\nPlease authenticate first !\n")
            exit()

        api_url = '{}/{}'.format(self.base_url, self.endpoint)
        response = requests.get(api_url,
                                headers=self.header, verify=self.verify)

        if response.status_code == 200:
            return (response.content.decode('utf-8'))

        else:
            print('[!]ERROR : HTTP {0} calling [{1}]'.format
                  (response.status_code, api_url))
            return response.content.decode('utf-8')

    def posts(self, endpoint, data):
        self.endpoint = endpoint
        self.header = {'Content-Type': 'application/json',
                       'Authorization': 'Bearer {0}'.format(self.token)}
        self.data = data
        if not self.token:
            print("Please authenticate first !")
            exit()

        api_url = '{}{}'.format(self.base_url, self.endpoint)
# if isinstance(self.data, str):
#    response = requests.post(api_url, data=self.data, verify=self.verify,
#    headers=self.header)
        if isinstance(self.data, dict):
            response = requests.post(api_url, json=self.data,
                                     verify=self.verify, headers=self.header)
            if response.status_code == 200:
                pass

            else:
                print('[!]ERROR : HTTP {0} calling [{1}]'.format
                      (response.status_code, api_url))

            return response.content.decode('utf-8')

        else:
            print("Data must a dictionary !!")
            sys.exit(-99)
