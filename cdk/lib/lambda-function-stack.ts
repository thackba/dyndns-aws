import * as cdk from "@aws-cdk/core";
import * as iam from "@aws-cdk/aws-iam";
import * as logs from "@aws-cdk/aws-logs";
import * as lambda from "@aws-cdk/aws-lambda";
import {domainName, domainNameHostedZoneIdOutput, lambdaDynDNSFunctionARNOutput} from "./names";

export class LambdaFunctionStack extends cdk.Stack {
    constructor(scope: cdk.Construct, props?: cdk.StackProps) {
        super(scope, "DynDnsAwsLambdaFunctionStack", props);

        // The code that defines your stack goes here

        const hostedZoneId = cdk.Fn.importValue(domainNameHostedZoneIdOutput);

        const lambdaDynDNSUpdate = "LambdaDynDNSUpdate";

        new logs.LogGroup(this, "LambdaDynDNSLogGroup", {
            logGroupName: "/aws/lambda/" + lambdaDynDNSUpdate,
            retention: logs.RetentionDays.FIVE_DAYS,
            removalPolicy: cdk.RemovalPolicy.DESTROY
        });

        const lambdaDynDNSRole = new iam.Role(this, "LambdaDynDNSRole", {
            roleName: "LambdaDynDNSRole",
            assumedBy: new iam.ServicePrincipal("lambda.amazonaws.com")
        });

        lambdaDynDNSRole.addManagedPolicy(
            iam.ManagedPolicy.fromAwsManagedPolicyName("service-role/AWSLambdaBasicExecutionRole")
        );

        lambdaDynDNSRole.attachInlinePolicy(new iam.Policy(this, "LambdaDynDnsRoleInlinePolicy", {
                statements: [
                    new iam.PolicyStatement({
                        effect: iam.Effect.ALLOW,
                        actions: [
                            "route53:ChangeResourceRecordSets"
                        ],
                        resources: [
                            `arn:aws:route53:::hostedzone/${hostedZoneId}`
                        ]
                    })
                ]
            })
        );

        const lambdaDynDNS = new lambda.Function(this, "LambdaDynDNSFunction", {
            functionName: lambdaDynDNSUpdate,
            runtime: lambda.Runtime.PYTHON_3_9,
            handler: "update_dns.handle",
            code: lambda.AssetCode.fromAsset("../package"),
            role: lambdaDynDNSRole,
            environment: {
                "DYNDNS_HOSTED_ZONE_ID": hostedZoneId,
                "DYNDNS_DOMAIN": domainName
            }
        })

        new cdk.CfnOutput(this, "LambdaDynDNSFunctionARNOutput", {
            exportName: lambdaDynDNSFunctionARNOutput,
            value: lambdaDynDNS.functionArn
        })
    }
}