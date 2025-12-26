import pathlib

import cdk_ecr_deployment as ecrdeploy
from aws_cdk import (
    Stack,
)
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_ecr_assets as ecr_assets
from constructs import Construct

TOP_DIRECTORY = str(pathlib.Path(__file__).parent.parent.parent)


class AgentcoreStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, prefix: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ecr_repository = ecr.Repository(self, "agent-ecr-repository", repository_name=f"{prefix}-agentcore-repository")

        docker_image = ecr_assets.DockerImageAsset(
            self, "agent-docker-image", directory=TOP_DIRECTORY, file="docker/images/agentcore/Dockerfile"
        )

        ecrdeploy.ECRDeployment(
            self,
            "agent-docker-image-deployment",
            src=ecrdeploy.DockerImageName(docker_image.image_uri),
            dest=ecrdeploy.DockerImageName(ecr_repository.repository_uri),
        )
