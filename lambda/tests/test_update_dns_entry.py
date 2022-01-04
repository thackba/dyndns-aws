import uuid
import boto3
import unittest
from moto import mock_route53

import update_dns
from tests.helper import create_zone, set_dns_value, get_records


@mock_route53
class UpdateDNSEntryTests(unittest.TestCase):

    def __init__(self, method_name: str = ...) -> None:
        super().__init__(method_name)
        self.domain = 'example.org'
        self.host_name = str(uuid.uuid4())
        self.fqdn_name = self.host_name + '.' + self.domain
        self.dns = boto3.client('route53')

    def test_create_new_ip4_only_entry(self):
        hosted_zone_id = create_zone(self.dns, self.domain)
        update_dns.update_dns_entry(
            hosted_zone_id, self.domain, self.host_name,
            ip4='192.168.100.10'
        )
        records = get_records(self.dns, hosted_zone_id, self.fqdn_name)
        self.assertEqual(records['A'], '192.168.100.10')
        self.assertFalse('AAAA' in records)

    def test_create_new_ip6_only_entry(self):
        hosted_zone_id = create_zone(self.dns, self.domain)
        update_dns.update_dns_entry(
            hosted_zone_id, self.domain, self.host_name,
            ip6='ff01::1'
        )
        records = get_records(self.dns, hosted_zone_id, self.fqdn_name)
        self.assertFalse('A' in records)
        self.assertEqual(records['AAAA'], 'ff01::1')

    def test_create_new_dual_ip_entry(self):
        hosted_zone_id = create_zone(self.dns, self.domain)
        update_dns.update_dns_entry(
            hosted_zone_id, self.domain, self.host_name,
            ip4='192.168.100.11',
            ip6='ff01::2'
        )
        records = get_records(self.dns, hosted_zone_id, self.fqdn_name)
        self.assertEqual(records['A'], '192.168.100.11')
        self.assertEqual(records['AAAA'], 'ff01::2')

    def test_update_ip4_only_entry(self):
        hosted_zone_id = create_zone(self.dns, self.domain)
        set_dns_value(
            self.dns, hosted_zone_id, self.fqdn_name,
            'A', '192.168.178.2'
        )
        set_dns_value(
            self.dns, hosted_zone_id, self.fqdn_name,
            'AAAA', 'ff01::3'
        )
        update_dns.update_dns_entry(
            hosted_zone_id, self.domain, self.host_name,
            ip4='192.168.178.10'
        )
        records = get_records(self.dns, hosted_zone_id, self.fqdn_name)
        self.assertEqual(records['A'], '192.168.178.10')
        self.assertEqual(records['AAAA'], 'ff01::3')

    def test_update_ip6_only_entry(self):
        hosted_zone_id = create_zone(self.dns, self.domain)
        set_dns_value(
            self.dns, hosted_zone_id, self.fqdn_name,
            'A', '192.168.178.3'
        )
        set_dns_value(
            self.dns, hosted_zone_id, self.fqdn_name,
            'AAAA', 'ff01::4'
        )
        update_dns.update_dns_entry(
            hosted_zone_id, self.domain, self.host_name,
            ip6='ff01::24'
        )
        records = get_records(self.dns, hosted_zone_id, self.fqdn_name)
        self.assertEqual(records['A'], '192.168.178.3')
        self.assertEqual(records['AAAA'], 'ff01::24')

    def test_update_dual_ip_entry(self):
        hosted_zone_id = create_zone(self.dns, self.domain)
        set_dns_value(
            self.dns, hosted_zone_id, self.fqdn_name,
            'A', '192.168.178.12'
        )
        set_dns_value(
            self.dns, hosted_zone_id, self.fqdn_name,
            'AAAA', 'ff01::32'
        )
        update_dns.update_dns_entry(
            hosted_zone_id, self.domain, self.host_name,
            ip4='192.168.188.12',
            ip6='ff01::43'
        )
        records = get_records(self.dns, hosted_zone_id, self.fqdn_name)
        self.assertEqual(records['A'], '192.168.188.12')
        self.assertEqual(records['AAAA'], 'ff01::43')

    def test_empty_entry_update(self):
        hosted_zone_id = create_zone(self.dns, self.domain)
        set_dns_value(
            self.dns, hosted_zone_id, self.fqdn_name,
            'A', '192.168.178.12'
        )
        set_dns_value(
            self.dns, hosted_zone_id, self.fqdn_name,
            'AAAA', 'ff01::32'
        )
        update_dns.update_dns_entry(
            hosted_zone_id, self.domain, self.host_name,
        )
        records = get_records(self.dns, hosted_zone_id, self.fqdn_name)
        self.assertEqual(records['A'], '192.168.178.12')
        self.assertEqual(records['AAAA'], 'ff01::32')


if __name__ == '__main__':
    unittest.main()
