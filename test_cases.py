#!/usr/bin/env python3

import cldpt 
import unittest
import json
import api

class MyTests(unittest.TestCase):
    def test1(self):
        self.maxDiff = None
        result = cldpt.run(["show", "reports"])
        expected_result = getattr(api.Command(), 'gets')('/reports')

        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
