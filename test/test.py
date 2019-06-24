#!/usr/bin/env python3

import os
import hashlib
import binascii
import unittest
import requests

CREATED = 201
OK = 200


def get_fresh_key():
    return b"http://localhost:3000/examplekey-" + binascii.hexlify(os.urandom(10))


class TestKVdb(unittest.TestCase):

    def test_get_put_delete(self):
        key = get_fresh_key()

        r = requests.post(key, data="examplevalue")
        self.assertEqual(r.status_code, CREATED)

        r = requests.get(key)
        self.assertEqual(r.status_code, OK)
        self.assertEqual(r.text, "examplevalue")

        r = requests.delete(key)
        self.assertEqual(r.status_code, OK)

    def test_delete(self):
        key = get_fresh_key()

        r = requests.post(key, data="examplevalue")
        self.assertEqual(r.status_code, CREATED)

        r = requests.delete(key)
        self.assertEqual(r.status_code, OK)

        r = requests.get(key)
        self.assertNotEqual(r.status_code, OK)

    def test_double_put(self):
        key = get_fresh_key()
        r = requests.post(key, data="examplevalue")
        self.assertEqual(r.status_code, CREATED)

        r = requests.put(key, data="examplevalue")
        self.assertNotEqual(r.status_code, CREATED)

    def test_10keys(self):
        keys = [get_fresh_key() for _ in range(10)]

        for k in keys:
            r = requests.post(k, data=hashlib.md5(k).hexdigest())
            self.assertEqual(r.status_code, CREATED)

        for k in keys:
            r = requests.get(k)
            self.assertEqual(r.status_code, OK)
            self.assertEqual(r.text, hashlib.md5(k).hexdigest())

        for k in keys:
            r = requests.delete(k)
            self.assertEqual(r.status_code, OK)


if __name__ == '__main__':
    unittest.main()
