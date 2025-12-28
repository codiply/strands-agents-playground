from aws_cdk import (
    Stack,
)
from aws_cdk import aws_iam as iam
from constructs import Construct
from common import AWS_ACCOUNT_ID, AWS_REGION_NAME


class BaseStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, prefix: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        tool_use_aws_role = iam.Role(
            self,
            "tool-use-aws-role",
            role_name=f"{prefix}-tool-use-aws",
            assumed_by=iam.CompositePrincipal(
                iam.AccountRootPrincipal(),
                iam.ServicePrincipal(
                    "bedrock-agentcore.amazonaws.com",
                    conditions={
                        "StringEquals": {"aws:SourceAccount": AWS_ACCOUNT_ID},
                        "ArnLike": {"aws:SourceArn": f"arn:aws:bedrock-agentcore:{AWS_REGION_NAME}:{AWS_ACCOUNT_ID}:*"},
                    },
                ),
            ),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("ReadOnlyAccess")],
        )

        self._tool_use_aws_role = tool_use_aws_role

    @property
    def tool_use_aws_role(self) -> iam.IRole:
        return self._tool_use_aws_role
