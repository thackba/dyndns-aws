import * as cdk from "@aws-cdk/core";
import * as route53 from "@aws-cdk/aws-route53";
import {domainName, domainNameHostedZoneIdOutput} from "./names";

export class DnsZoneStack extends cdk.Stack {
    constructor(scope: cdk.Construct, props?: cdk.StackProps) {
        super(scope, "DynDnsAwsDnsZoneStack", props);

        // The code that defines your stack goes here

        const zone = new route53.HostedZone(this, "DnsZone", {
            zoneName: domainName
        })

        new cdk.CfnOutput(this, "DnsZoneIdOutput", {
            exportName: domainNameHostedZoneIdOutput,
            value: zone.hostedZoneId
        })
    }
}
