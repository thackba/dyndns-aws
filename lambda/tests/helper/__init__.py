def create_zone(client, domain):
    response = client.create_hosted_zone(
        Name=domain,
        CallerReference=str(hash('create domain'))
    )
    return response['HostedZone']['Id']


def delete_zone(client, hosted_zone_id):
    client.delete_hosted_zone(
        Id=hosted_zone_id
    )


def set_dns_value(client, hosted_zone_id, host_name, dns_type, value):
    client.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            'Changes': [{
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': host_name,
                    'Type': dns_type,
                    'TTL': 60,
                    'ResourceRecords': [{'Value': value}],
                },
            }]
        }
    )


def delete_dns_value(client, hosted_zone_id, host_name, dns_type):
    client.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            'Changes': [{
                'Action': 'DELETE',
                'ResourceRecordSet': {
                    'Name': host_name,
                    'Type': dns_type,
                },
            }]
        }
    )


def get_records(client, hosted_zone_id, host_name):
    records = client.list_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        StartRecordName=host_name,
    )
    return {x['Type']: x['ResourceRecords'][0]['Value'] for x in
            records['ResourceRecordSets']}
