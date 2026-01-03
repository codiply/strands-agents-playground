from aws_cdk import (
    Stack,
)
from aws_cdk import aws_iam as iam
from constructs import Construct


class BaseStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, prefix: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        tool_use_aws_role = iam.Role(
            self,
            "tool-use-aws-role",
            role_name=f"{prefix}-tool-use-aws",
            assumed_by=iam.AccountRootPrincipal(),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("ReadOnlyAccess")],
        )

        self._tool_use_aws_role = tool_use_aws_role

    @property
    def tool_use_aws_role(self) -> iam.IRole:
        return self._tool_use_aws_role
