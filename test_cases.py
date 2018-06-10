#!/usr/bin/env python3

import unittest
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from constants import GETS_DICT
import cldpt
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

IMPLEMENTED = ["report-types", "schedules", "granules"]


class MyTests(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.endpoint = ''
        self.ip_addr = '127.0.0.1'
        self.base_url = 'https://' + self.ip_addr + ':/cloudpoint/api/v2'
        self.verify = False
        try:
            with open("/root/.cldpt_token", "r") as file_handle:
                self.token = file_handle.readline()
        except FileNotFoundError:
            self.token = ''

        self.header = {'Content-Type': 'application/json',
                       'Authorization': 'Bearer {0}'.format(self.token)}

    def test_gets(self):
        for key, value in GETS_DICT.items():
            if key not in IMPLEMENTED:
                self.endpoint = value
                api_url = '{}/{}'.format(self.base_url, self.endpoint)
                response = requests.get(api_url, headers=self.header,
                                        verify=self.verify)
                expected_result = response.content.decode('utf-8')
                if key == 'smtp':
                    result = cldpt.run(["show", 'settings', 'smtp'])
                elif key == 'ad':
                    result = cldpt.run(["show", 'settings', 'ad'])
                else:
                    result = cldpt.run(["show", key])
                with self.subTest(key=key):
                    self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
