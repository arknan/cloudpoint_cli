#!/usr/bin/env python3

import requests 
import json
import getpass
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



class Command():

    def __init__(self) :
        self.endpoint = ''
        self.base_url = 'https://127.0.0.1:/cloudpoint/api/v2'
        self.verify = False
        try :
            with open("/root/.cldpt_token", "r") as file_handle :
                self.token = file_handle.readline()
        except FileNotFoundError :
            self.token = ''
        self.header = {'Content-Type': 'application/json',
                    'Authorization': 'Bearer {0}'.format(self.token)}

    def authenticate(self) :
        self.base_url = 'https://127.0.0.1:/cloudpoint/api/v2'
        self.token_endpoint = '/idm/login'
        self.verify = False
        headers = {'Content-Type': 'application/json'}
        self.endpoint= self.base_url + self.token_endpoint
        username = input("Username: ")
        passwd = getpass.getpass("Password: ")
        data = json.dumps({
            "email": username,
            "password": passwd})
            
        response = requests.post(self.endpoint, verify=self.verify, headers=headers, data=data)
        if response.status_code == 200 :
           self.token = ( (json.loads(response.content.decode('utf-8')))["accessToken"] )
           with open("/root/.cldpt_token", "w") as file_handle:
               file_handle.write(self.token)
        else :
            print( (json.loads(response.content.decode('utf-8'))["errorMessage"]))


    def gets(self):
        if not self.token :
            print("Please authenticate first !")
            exit()

        api_url = '{}/{}'.format(self.base_url, self.endpoint)
        r = requests.get(api_url, headers=self.header, verify=self.verify)

        if r.status_code == 200 :
            print (r.content.decode('utf-8'))
        else :
            print ('[!]ERROR : HTTP {0} calling [{1}]'. format(r.status_code, api_url))
            print("\n\nDETAILS : \n ", r.content.decode('utf-8'))

    def posts(self):
        if not self.token :
            print("Please authenticate first !")
            exit()

        api_url = '{}/reports/'.format(self.base_url)
        data="""{
               "reportId": "pypy",
               "reportType": "snapshot",
               "columns": ["id", "name", "region", "ctime"]
        }"""
        r = requests.post(api_url, data=data, verify=False, headers=self.header)
        val = json.loads((r.content.decode('utf-8')))
        print(val['msg'])


if __name__ == '__main__' :
    x = Command()
 #   x.authenticate()
    print('from self.token\n')
    print(x.token)
"""
    y = ['gets', 'puts']
    x = Command()
    result = getattr(x, y[0])
    if callable(result):
        result()
    else :
        print("something went wrong :( ")


    #posts()
"""
