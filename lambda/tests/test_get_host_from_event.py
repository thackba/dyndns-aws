import unittest
import update_dns


class GetHostNameFromEventTests(unittest.TestCase):

    def __init__(self, method_name: str = ...) -> None:
        super().__init__(method_name)

    def test_get_valid_host_name(self):
        event = {'queryStringParameters': {'host': 'hostname'}}
        hostname = update_dns.get_host_name_from_event(event)
        self.assertEqual(hostname, 'hostname')

    def test_missing_host_name(self):
        event = {}
        hostname = update_dns.get_host_name_from_event(event)
        self.assertTrue(hostname is None)

    def test_too_short_host_name(self):
        event = {'queryStringParameters': {'host': 'abcd'}}
        hostname = update_dns.get_host_name_from_event(event)
        self.assertTrue(hostname is None)

    def test_too_long_host_name(self):
        event = {'queryStringParameters': {'host': 'abcdefghi'}}
        hostname = update_dns.get_host_name_from_event(event)
        self.assertTrue(hostname is None)

    def test_wrong_host_name(self):
        event = {'queryStringParameters': {'host': '123456'}}
        hostname = update_dns.get_host_name_from_event(event)
        self.assertTrue(hostname is None)