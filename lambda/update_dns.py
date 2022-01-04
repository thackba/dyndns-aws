import os
import re
import boto3
import ipaddress

hostname_pattern = re.compile('^[a-z]{5,8}$')


def handle(event, _):
    domain = os.environ['DYNDNS_DOMAIN']
    hosted_zone_id = os.environ['DYNDNS_HOSTED_ZONE_ID']
    host_name = get_host_name_from_event(event)
    (ip4, ip6) = get_ips_from_event(event)
    print(event['queryStringParameters'], host_name, ip4, ip6)
    if host_name is not None:
        if ip4 is not None or ip6 is not None:
            update_dns_entry(hosted_zone_id, domain, host_name, ip4, ip6)
            return {
                'statusCode': 200,
            }
    return {
        'statusCode': 400,
    }


def get_host_name_from_event(event):
    host_name = None
    if 'queryStringParameters' in event:
        params = event['queryStringParameters']
        if 'host' in params:
            maybe_host = params['host']
            if hostname_pattern.match(maybe_host) is not None:
                host_name = maybe_host
    return host_name


def get_ips_from_event(event):
    ip4, ip6 = None, None
    if 'queryStringParameters' in event:
        params = event['queryStringParameters']
        if 'ip4' in params:
            maybe_ip4 = params['ip4']
            if is_ipaddress(maybe_ip4):
                ip4 = maybe_ip4
        if 'ip6' in params:
            maybe_ip6 = params['ip6']
            if is_ipaddress(maybe_ip6):
                ip6 = maybe_ip6
    return ip4, ip6


def is_ipaddress(address):
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False


def update_dns_entry(hosted_zone_id, domain, host_name, ip4=None, ip6=None):
    client = boto3.client('route53')
    changes = []
    if ip4 is not None:
        changes.append(build_upsert_change(domain, host_name, 'A', ip4))
    if ip6 is not None:
        changes.append(build_upsert_change(domain, host_name, 'AAAA', ip6))
    if len(changes) > 0:
        response = client.change_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            ChangeBatch={
                'Changes': changes
            }
        )
        print(response)


def build_upsert_change(domain, host_name, dns_type, ip_value):
    return {
        'Action': 'UPSERT',
        'ResourceRecordSet': {
            'Name': host_name + '.' + domain,
            'Type': dns_type,
            'TTL': 60,
            'ResourceRecords': [{'Value': ip_value}],
        }
    }
