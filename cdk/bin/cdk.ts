#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "@aws-cdk/core";
import {DnsZoneStack} from "../lib/dns-zone-stack";
import {LambdaFunctionStack} from "../lib/lambda-function-stack";
import {ApiGatewayStack} from "../lib/api-gateway-stack";

const env = {account: process.env.CDK_DEFAULT_ACCOUNT, region: process.env.CDK_DEFAULT_REGION}

const app = new cdk.App();

new DnsZoneStack(app, {env});
new LambdaFunctionStack(app, {env})
new ApiGatewayStack(app, {env})