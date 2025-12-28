#!/usr/bin/env python3
import aws_cdk as cdk
from common import AWS_ACCOUNT_ID, AWS_REGION_NAME
from stacks.agentcore import AgentcoreStack
from stacks.base import BaseStack

PREFIX = "strands-playground"

app = cdk.App()

base_stack = BaseStack(
    app,
    f"{PREFIX}-base",
    prefix=PREFIX,
    env=cdk.Environment(account=AWS_ACCOUNT_ID, region=AWS_REGION_NAME),
)

agent_core_stack = AgentcoreStack(
    app,
    f"{PREFIX}-agentcore",
    prefix=PREFIX,
    tool_use_aws_role=base_stack.tool_use_aws_role,
    env=cdk.Environment(account=AWS_ACCOUNT_ID, region=AWS_REGION_NAME),
)
agent_core_stack.add_dependency(base_stack)

app.synth()
