import pathlib

import aws_cdk as cdk
import cdk_ecr_deployment as ecrdeploy
from aws_cdk import (
    Stack,
)
from aws_cdk import aws_bedrockagentcore as bedrockagentcore
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_ecr_assets as ecr_assets
from aws_cdk import aws_iam as iam
from common import AWS_ACCOUNT_ID, AWS_REGION_NAME
from constructs import Construct

TOP_DIRECTORY = str(pathlib.Path(__file__).parent.parent.parent)

AGENT_TOOL_USE_AWS_PROFILE_NAME = "strands-playground-tool-use-aws"


class AgentcoreStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, prefix: str, tool_use_aws_role: iam.IRole, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ecr_repository = ecr.Repository(
            self,
            "agent-ecr-repository",
            repository_name=f"{prefix}-agentcore-repository",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            empty_on_delete=True,
        )

        docker_image = ecr_assets.DockerImageAsset(
            self,
            "agent-docker-image",
            directory=TOP_DIRECTORY,
            file="docker/images/agentcore/Dockerfile",
            build_args={
                "AWS_ACCOUNT_ID": AWS_ACCOUNT_ID,
                "AWS_REGION_NAME": AWS_REGION_NAME,
                "AGENT_TOOL_USE_AWS_PROFILE_NAME": AGENT_TOOL_USE_AWS_PROFILE_NAME,
            },
        )

        ecr_deployment = ecrdeploy.ECRDeployment(
            self,
            "agent-docker-image-deployment",
            src=ecrdeploy.DockerImageName(docker_image.image_uri),
            dest=ecrdeploy.DockerImageName(ecr_repository.repository_uri),
        )

        agentcore_runtime_role = iam.Role(
            self,
            "agentcore-runtime-role",
            role_name=f"{prefix}-agentcore-runtime-role",
            assumed_by=iam.ServicePrincipal(
                "bedrock-agentcore.amazonaws.com",
                conditions={
                    "StringEquals": {"aws:SourceAccount": AWS_ACCOUNT_ID},
                    "ArnLike": {"aws:SourceArn": f"arn:aws:bedrock-agentcore:{AWS_REGION_NAME}:{AWS_ACCOUNT_ID}:*"},
                },
            ),
            inline_policies={
                "AgentCorePolicy": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            sid="ECRImageAccess",
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "ecr:BatchGetImage",
                                "ecr:GetDownloadUrlForLayer",
                                "ecr:BatchCheckLayerAvailability",
                            ],
                            resources=[f"arn:aws:ecr:{AWS_REGION_NAME}:{AWS_ACCOUNT_ID}:repository/*"],
                        ),
                        iam.PolicyStatement(
                            sid="ECRTokenAccess",
                            effect=iam.Effect.ALLOW,
                            actions=["ecr:GetAuthorizationToken"],
                            resources=["*"],
                        ),
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "logs:DescribeLogStreams",
                                "logs:CreateLogGroup",
                                "logs:DescribeLogGroups",
                                "logs:CreateLogStream",
                                "logs:PutLogEvents",
                            ],
                            resources=[
                                (
                                    f"arn:aws:logs:{AWS_REGION_NAME}:{AWS_ACCOUNT_ID}:"
                                    "log-group:/aws/bedrock-agentcore/runtimes/*"
                                )
                            ],
                        ),
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "xray:PutTraceSegments",
                                "xray:PutTelemetryRecords",
                                "xray:GetSamplingRules",
                                "xray:GetSamplingTargets",
                            ],
                            resources=["*"],
                        ),
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=["cloudwatch:PutMetricData"],
                            resources=["*"],
                            conditions={"StringEquals": {"cloudwatch:namespace": "bedrock-agentcore"}},
                        ),
                        iam.PolicyStatement(
                            sid="GetAgentAccessToken",
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "bedrock-agentcore:GetWorkloadAccessToken",
                                "bedrock-agentcore:GetWorkloadAccessTokenForJWT",
                                "bedrock-agentcore:GetWorkloadAccessTokenForUserId",
                            ],
                            resources=[
                                (
                                    f"arn:aws:bedrock-agentcore:{AWS_REGION_NAME}:{AWS_ACCOUNT_ID}:"
                                    "workload-identity-directory/default"
                                ),
                                (
                                    f"arn:aws:bedrock-agentcore:{AWS_REGION_NAME}:{AWS_ACCOUNT_ID}:"
                                    "workload-identity-directory/default/workload-identity/*"
                                ),
                            ],
                        ),
                        iam.PolicyStatement(
                            sid="BedrockModelInvocation",
                            effect=iam.Effect.ALLOW,
                            actions=["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
                            resources=[
                                "arn:aws:bedrock:*::foundation-model/*",
                                f"arn:aws:bedrock:{AWS_REGION_NAME}:{AWS_ACCOUNT_ID}:*",
                            ],
                        ),
                        iam.PolicyStatement(
                            sid="AssumeToolUseAwsRole",
                            effect=iam.Effect.ALLOW,
                            actions=["sts:AssumeRole"],
                            resources=[tool_use_aws_role.role_arn],
                        ),
                    ]
                )
            },
        )

        agentcore_runtime = bedrockagentcore.CfnRuntime(
            self,
            "agentcore-runtime",
            agent_runtime_artifact=bedrockagentcore.CfnRuntime.AgentRuntimeArtifactProperty(
                container_configuration=bedrockagentcore.CfnRuntime.ContainerConfigurationProperty(
                    container_uri=ecr_repository.repository_uri_for_tag("latest")
                )
            ),
            agent_runtime_name=f"{prefix.replace("-", "_")}_agentcore_runtime",
            network_configuration=bedrockagentcore.CfnRuntime.NetworkConfigurationProperty(
                network_mode="PUBLIC",
            ),
            role_arn=agentcore_runtime_role.role_arn,
            description="Runtime for playground agent",
            environment_variables={
                "AGENT_TOOL_USE_AWS_PROFILE_NAME": AGENT_TOOL_USE_AWS_PROFILE_NAME,
            },
            lifecycle_configuration=bedrockagentcore.CfnRuntime.LifecycleConfigurationProperty(
                idle_runtime_session_timeout=10 * 60, max_lifetime=60 * 60
            ),
            protocol_configuration="HTTP",
        )
        agentcore_runtime.node.add_dependency(ecr_deployment)

        bedrockagentcore.CfnRuntimeEndpoint(
            self,
            "agentcore-runtime-endpoint",
            agent_runtime_id=agentcore_runtime.attr_agent_runtime_id,
            name=f"{prefix.replace("-", "_")}_agentcore_runtime_endpoint",
        )
