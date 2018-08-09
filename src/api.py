#!/usr/bin/env python3


import configparser
import json
import sys
from getpass import getpass
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)


class Command():

    def __init__(self):

        config = configparser.ConfigParser()
        if not config.read('/root/.cloudpoint_cli.config'):
            print("\ncloudpoint_cli.config is empty or missing\n")
            sys.exit(-1)
        try:
            self.ip_addr = config['GLOBAL']['cloudpoint_ip']
            self.token_file = config['GLOBAL']['cp_token_file']
        except KeyError:
            print("Please ensure config file has 'cloudpoint_ip' & 'cp_token_file' values\n")
            sys.exit(-1)

        try:
            self.username = config['GLOBAL']['cloudpoint_username']
            self.password = config['GLOBAL']['cloudpoint_password']
        except KeyError:
            self.username = None
            self.password = None

        self.endpoint = None
        self.base_url = 'https://' + self.ip_addr + ':/cloudpoint/api/v2'
        self.api_url = '{}{}'.format(self.base_url, self.endpoint)
        self.verify = False
        self.data = None
        try:
            with open(self.token_file, "r") as file_handle:
                self.token = file_handle.readline()
        except FileNotFoundError:
            self.token = None

        self.header = {'Content-Type': 'application/json',
                       'Authorization': 'Bearer {0}'.format(self.token)}

        self.token_header = {'Content-Type': 'application/json'}
        self.token_endpoint = self.base_url + '/idm/login'


    def authenticates(self):

        if not (self.username and self.password):
            self.username = input("Username: ")
            self.password = getpass("Password: ")

        self.data = json.dumps({
            "email": self.username,
            "password": self.password})

        response = requests.post(self.token_endpoint, verify=self.verify,
                                 headers=self.token_header, data=self.data)
        if response.status_code == 200:
            self.token = json.loads(
                response.content.decode('utf-8'))["accessToken"]

            try:
                with open(self.token_file, "w") as file_handle:
                    file_handle.write(self.token)
            except:
                print("Error opening {}".format(self.token_file))

            print("Authentication Success !!")

        else:
            print(json.loads(response.content.decode('utf-8'))["errorMessage"])
            sys.exit(-1)

    def deletes(self, endpoint):
        self.verify_token()
        self.endpoint = endpoint
        self.api_url = '{}{}'.format(self.base_url, self.endpoint)

        response = requests.delete(
            self.api_url, verify=self.verify, headers=self.header)

        return response.content.decode('utf-8')

    def gets(self, endpoint):
        self.verify_token()
        self.endpoint = endpoint
        self.api_url = '{}{}'.format(self.base_url, self.endpoint)

        response = requests.get(
            self.api_url, headers=self.header, verify=self.verify)

        return response.content.decode('utf-8')

    def patches(self, endpoint, data):
        self.verify_token()
        self.endpoint = endpoint
        self.api_url = '{}{}'.format(self.base_url, self.endpoint)

        response = requests.patch(
            self.api_url, verify=self.verify, headers=self.header)

        return response.content.decode('utf-8')

    def posts(self, endpoint, data):
        self.verify_token()
        self.endpoint = endpoint
        self.api_url = '{}{}'.format(self.base_url, self.endpoint)
        self.data = data

        response = requests.post(
            self.api_url, json=self.data, verify=self.verify, headers=self.header)

        return response.content.decode('utf-8')

    def puts(self, endpoint, data):
        self.verify_token()
        self.endpoint = endpoint
        self.api_url = '{}{}'.format(self.base_url, self.endpoint)
        self.data = data

        response = requests.put(
            self.api_url, json=self.data, verify=self.verify, headers=self.header)

        return response.content.decode('utf-8')

        
    def verify_token(self):
        self.endpoint = '/version'
        self.api_url = '{}{}'.format(self.base_url, self.endpoint)
        if not self.token:
            print("Please authenticate first !")
            sys.exit(-1)

        try:
            response = requests.get(
                self.api_url, headers=self.header, verify=self.verify)
        except requests.exceptions.ConnectionError:
            print("\nConnection timed out. Verify if :\n\
1)CloudPoint server's IP address is {}\n---> Update config file if it isn't\n\
2)Port 443 is open at both ends\n ".format(self.ip_addr))
            sys.exit(-1)
        except ValueError:
            print("Invalid token !\nPlease Authenticate again")
            sys.exit(-1)

        return True
