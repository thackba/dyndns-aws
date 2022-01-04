import * as cdk from '@aws-cdk/core';
import {Template} from '@aws-cdk/assertions';
import {DnsZoneStack} from '../lib/dns-zone-stack';
import {domainName} from "../lib/names";

test('Hosted Zone created', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new DnsZoneStack(app)
    // THEN
    const template = Template.fromStack(stack);

    template.hasResourceProperties('AWS::Route53::HostedZone', {
        Name: `${domainName}.`
    });
});
