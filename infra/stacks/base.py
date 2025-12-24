from aws_cdk import (
    Stack,
)
from aws_cdk import aws_iam as iam
from constructs import Construct


class BaseStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, prefix: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        iam.Role(
            self,
            "tool-use-aws-role",
            role_name=f"{prefix}-tool-use-aws",
            assumed_by=iam.AccountRootPrincipal(),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("ReadOnlyAccess")],
        )
