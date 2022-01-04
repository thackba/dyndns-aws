import * as cdk from "@aws-cdk/core";
import * as iam from "@aws-cdk/aws-iam";
import * as lambda from "@aws-cdk/aws-lambda";
import * as apiGateway from "@aws-cdk/aws-apigateway";
import {lambdaDynDNSFunctionARNOutput} from "./names";

export class ApiGatewayStack extends cdk.Stack {
    constructor(scope: cdk.Construct, props?: cdk.StackProps) {
        super(scope, "DynDnsAwsApiGatewayStack", props);

        // The code that defines your stack goes here

        const functionArn = cdk.Fn.importValue(lambdaDynDNSFunctionARNOutput);

        const gateway = new apiGateway.RestApi(this, "Gateway", {
            restApiName: "dyndns-gateway",
            endpointExportName: "DynDNSAPIGateway",
            defaultMethodOptions: {
                apiKeyRequired: false
            }
        });

        const gatewayRole = new iam.Role(this, "GatewayRole", {
            roleName: "DynDNSGatewayRole",
            assumedBy: new iam.ServicePrincipal("apigateway.amazonaws.com")
        })

        gatewayRole.attachInlinePolicy(new iam.Policy(this, "GatewayRolePolicy", {
            statements: [
                new iam.PolicyStatement({
                    effect: iam.Effect.ALLOW,
                    actions: ["lambda:InvokeFunction"],
                    resources: [functionArn]
                })
            ]
        }))

        const updateResource = new apiGateway.Resource(this, "GatewayUpdateResource", {
            parent: gateway.root,
            pathPart: "update"
        });

        const updateLambda = lambda.Function.fromFunctionArn(this, "GatewayUpdateFunction", functionArn);

        const updateIntegration = new apiGateway.LambdaIntegration(updateLambda, {
            credentialsRole: gatewayRole
        });

        new apiGateway.Method(this, "GatewayUpdateMethod", {
            httpMethod: "POST",
            resource: updateResource,
            integration: updateIntegration
        });
    }
}