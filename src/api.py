#!/usr/bin/env python3


import configparser
import json
import os
import sys
from getpass import getpass
import logs
try:
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except ImportError:
    print("Please install requests for python3 and try again\n")


class Command():

    def __init__(self):

        self.log_f = logs.setup(__name__, 'f')
        self.log_c = logs.setup(__name__, 'c')
        self.log_fc = logs.setup(__name__)

        config = configparser.ConfigParser()
        config.read('/root/.cloudpoint_cli.config')
        try:
            self.ip_addr = config['GLOBAL']['cloudpoint_ip']
            self.log_f.debug(
                "CP server IP found from config file : '%s'", self.ip_addr)
            self.token_file = config['GLOBAL']['cp_token_file']
        except KeyError:
            self.log_fc("Please ensure config file has 'cloudpoint_ip' &\
'cp_token_file' values")
            sys.exit(1)

        try:
            self.username = config['GLOBAL']['cloudpoint_username']
        except KeyError:
            self.username = None
        try:
            self.password = config['GLOBAL']['cloudpoint_password']
        except KeyError:
            self.password = None

        self.endpoint = None
        self.base_url = 'https://' + self.ip_addr + ':/cloudpoint/api/v2'
        self.api_url = '{}{}'.format(self.base_url, self.endpoint)
        self.log_f.debug(
            "Base URL used for API queries : '%s'", self.base_url)
        self.verify = False
        self.data = None
        try:
            with open(self.token_file, "r") as file_handle:
                self.token = file_handle.readline()
        except FileNotFoundError as fnfe:
            self.log_f.debug(
                "File '%s' not found\n%s", self.token_file, fnfe)
            self.token = None

        self.header = {'Content-Type': 'application/json',
                       'Authorization': 'Bearer {0}'.format(self.token)}

        self.token_header = {'Content-Type': 'application/json'}
        self.token_endpoint = self.base_url + '/idm/login'

    def authenticates(self):

        if not self.username:
            self.username = input("Username: ")
        if not self.password:
            self.password = getpass("Password for user {}: ".format(
                self.username))

        self.log_f.info("Authenticating user '%s'", self.username)

        self.data = json.dumps({
            "email": self.username,
            "password": self.password})

        try:
            response = requests.post(self.token_endpoint, verify=self.verify,
                                     headers=self.token_header, data=self.data)

        except requests.exceptions.ConnectionError:
            self.log_fc.error("Connection timed out. Verify if :\n\
1)CloudPoint server's IP address is %s\n---> Update config file if it isn't\n\
2)Port 443 is open at both ends\n3)Verify if CloudPoint is running\n",
                              self.ip_addr)
            sys.exit(1)

        except ValueError:
            self.log_c.error("Invalid token! Please Authenticate again\n")
            sys.exit(1)

        self.log_f.debug(
            "Received status code '%s' for AUTHENTICATE", response.status_code)
        if response.status_code == 200:
            self.token = json.loads(
                response.content.decode('utf-8'))["accessToken"]

            try:
                with open(self.token_file, "w") as file_handle:
                    file_handle.write(self.token)
            except FileNotFoundError as fnfe:
                self.log_fc.error(
                    "Error writing to '%s'\n%s", self.token_file, fnfe)
                sys.exit(1)

            self.log_c.info("Authentication Success !!")

        else:
            self.log_fc.error(json.loads(
                response.content.decode('utf-8'))["errorMessage"])
            sys.exit(1)

    def deletes(self, endpoint):
        self.verify_token()
        self.endpoint = endpoint
        self.api_url = '{}{}'.format(self.base_url, self.endpoint)
        self.log_f.debug("Calling DELETE on '%s'", self.api_url)

        try:
            response = requests.delete(
                self.api_url, verify=self.verify, headers=self.header)

        except requests.exceptions.ConnectionError:
            self.log_fc.error("Connection timed out. Verify if :\n\
1)CloudPoint server's IP address is %s\n---> Update config file if it isn't\n\
2)Port 443 is open at both ends\n3)Verify if CloudPoint is running\n",
                              self.ip_addr)
            sys.exit(1)

        except ValueError:
            self.log_c.error("Invalid token! Please Authenticate again")
            sys.exit(1)

        self.log_f.debug("Received '%s' for DELETE", response.status_code)

        return response.content.decode('utf-8')

    def gets(self, endpoint):
        self.verify_token()
        self.endpoint = endpoint
        self.api_url = '{}{}'.format(self.base_url, self.endpoint)
        self.log_f.debug("Calling GET on '%s'", self.api_url)

        try:
            response = requests.get(
                self.api_url, headers=self.header, verify=self.verify)

        except requests.exceptions.ConnectionError:
            self.log_fc.error("Connection timed out. Verify if :\n\
1)CloudPoint server's IP address is %s\n---> Update config file if it isn't\n\
2)Port 443 is open at both ends\n3)Verify if CloudPoint is running\n",
                              self.ip_addr)
            sys.exit(1)

        except ValueError:
            self.log_c.error("Invalid token! Please Authenticate again")
            sys.exit(1)

        self.log_f.debug("Received '%s' for GET on %s", response.status_code,
                         self.api_url)

        return response.content.decode('utf-8')

    def patches(self, endpoint, data):
        self.verify_token()
        self.data = data
        self.endpoint = endpoint
        self.api_url = '{}{}'.format(self.base_url, self.endpoint)
        self.log_f.debug("Calling PATCH on '%s'", self.api_url)

        try:
            response = requests.patch(
                self.api_url, verify=self.verify, headers=self.header)

        except requests.exceptions.ConnectionError:
            self.log_fc.error("Connection timed out. Verify if :\n\
1)CloudPoint server's IP address is %s\n---> Update config file if it isn't\n\
2)Port 443 is open at both ends\n3)Verify if CloudPoint is running\n",
                              self.ip_addr)
            sys.exit(1)

        except ValueError:
            self.log_c.error("Invalid token! Please Authenticate again")
            sys.exit(1)

        self.log_f.debug("Received '%s' for PATCH", response.status_code)

        return response.content.decode('utf-8')

    def posts(self, endpoint, data):
        self.verify_token()
        self.data = data
        self.endpoint = endpoint
        self.api_url = '{}{}'.format(self.base_url, self.endpoint)
        self.log_f.debug(
            "Calling POST on '%s' with data : %s", self.api_url, self.data)

        try:
            response = requests.post(self.api_url, json=self.data,
                                     verify=self.verify, headers=self.header)

        except requests.exceptions.ConnectionError:
            self.log_fc.error("Connection timed out. Verify if :\n\
1)CloudPoint server's IP address is %s\n---> Update config file if it isn't\n\
2)Port 443 is open at both ends\n3)Verify if CloudPoint is running\n",
                              self.ip_addr)
            sys.exit(1)

        except ValueError:
            self.log_c.error("Invalid token! Please Authenticate again")
            sys.exit(1)

        self.log_f.debug("Received '%s' for POST", response.status_code)

        return response.content.decode('utf-8')

    def puts(self, endpoint, data):
        self.verify_token()
        self.data = data
        self.endpoint = endpoint
        self.api_url = '{}{}'.format(self.base_url, self.endpoint)
        self.log_f.debug(
            "Calling PUT on '%s' with data %s", self.api_url, self.data)
        try:
            response = requests.put(self.api_url, json=self.data,
                                    verify=self.verify, headers=self.header)

        except requests.exceptions.ConnectionError:
            self.log_fc.error("Connection timed out. Verify if :\n\
1)CloudPoint server's IP address is %s\n---> Update config file if it isn't\n\
2)Port 443 is open at both ends\n3)Verify if CloudPoint is running\n",
                              self.ip_addr)
            sys.exit(1)

        except ValueError:
            self.log_c.error("Invalid token! Please Authenticate again")
            sys.exit(1)

        self.log_f.debug("Received '%s' for PUT", response.status_code)

        return response.content.decode('utf-8')

    def verify_token(self):

        if not self.token:
            self.log_c.error("Please authenticate first !")
            self.authenticates()

        return True


def check_attr(args, attr):
    try:
        return bool(getattr(args, attr))
    except (NameError, IndexError, KeyError, AttributeError):
        return False


def get_stty_cols():

    ROWS, COLUMNS = os.popen('stty size', 'r').read().split()

    return int(COLUMNS)
