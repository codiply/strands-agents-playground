#!/usr/bin/env python3
import os

import aws_cdk as cdk
from stacks.agentcore import AgentcoreStack
from stacks.base import BaseStack

PREFIX = "strands-playground"

app = cdk.App()

CDK_ACCOUNT_ID = os.getenv("CDK_ACCOUNT_ID")
CDK_REGION_NAME = os.getenv("CDK_REGION_NAME")

BaseStack(
    app,
    f"{PREFIX}-base",
    prefix=PREFIX,
    env=cdk.Environment(account=CDK_ACCOUNT_ID, region=CDK_REGION_NAME),
)

AgentcoreStack(
    app,
    f"{PREFIX}-agentcore",
    prefix=PREFIX,
    env=cdk.Environment(account=CDK_ACCOUNT_ID, region=CDK_REGION_NAME),
)

app.synth()
