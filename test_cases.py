#!/usr/bin/env python3

import unittest
import json
import cldpt 
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings()


implemented = ["reports", "privileges", "assets", "agents"]

class MyTests(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.endpoint = ''
        self.ip = '127.0.0.1'
        self.base_url = 'https://' + self.ip + ':/cloudpoint/api/v2'
        self.verify = False
        try:
            with open("/root/.cldpt_token", "r") as file_handle:
                self.token = file_handle.readline()
        except FileNotFoundError:
            self.token = ''

        self.header = {'Content-Type': 'application/json',
                       'Authorization': 'Bearer {0}'.format(self.token)}


    def test_reports(self):
        for k,v in cldpt.GETS_DICT.items():
            if k in implemented : 
                self.endpoint = v
                api_url = '{}/{}'.format(self.base_url, self.endpoint)
                response = requests.get(api_url, headers=self.header, verify=self.verify)
                expected_result = response.content.decode('utf-8')
                result = cldpt.run(["show", k])
                with self.subTest(k=k):
                    self.assertEqual(result, expected_result)

    def prib(self):
        result = cldpt.run(["show", "privileges"])
        expected_result = getattr(api.Command(), 'gets')('/authorization/privilege')

        self.assertEqual(result, expected_result)

        result = cldpt.run(["show", "privileges", "-i", "e560b949-5f8b-42a5-8489-0e98368b2498"])
        expected_result = getattr(api.Command(), 'gets')('/authorization/privilege/e560b949-5f8b-42a5-8489-0e98368b2498')

        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
