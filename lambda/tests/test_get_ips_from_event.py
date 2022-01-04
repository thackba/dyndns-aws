import unittest
import update_dns


def get_event(ip4, ip6):
    params = {}
    if ip4 is not None:
        params['ip4'] = ip4
    if ip6 is not None:
        params['ip6'] = ip6
    return {'queryStringParameters': params}


class GetIpsFromEventTests(unittest.TestCase):

    def __init__(self, method_name: str = ...) -> None:
        super().__init__(method_name)

    def test_empty_ips(self):
        (ip4, ip6) = update_dns.get_ips_from_event(get_event(None, None))
        self.assertTrue(ip4 is None)
        self.assertTrue(ip6 is None)

    def test_valid_ips(self):
        (ip4, ip6) = update_dns.get_ips_from_event(
            get_event('127.0.0.1', 'ff01::4'))
        self.assertEqual(ip4, '127.0.0.1')
        self.assertEqual(ip6, 'ff01::4')

    def test_invalid_ips(self):
        (ip4, ip6) = update_dns.get_ips_from_event(
            get_event('277.0.0.1', 'ff..01::4'))
        self.assertTrue(ip4 is None)
        self.assertTrue(ip6 is None)
