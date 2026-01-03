from strands import Agent
from strands.models import BedrockModel
from strands_tools import current_time, use_aws

from playground.agents.hooks.use_aws import UseAwsInterceptor

MODEL_ID = "eu.amazon.nova-micro-v1:0"
# MODEL_ID="eu.amazon.nova-pro-v1:0"


def build_agent() -> Agent:
    bedrock_model = BedrockModel(
        model_id=MODEL_ID,
        temperature=0.3,
        # streaming=True,
    )

    agent = Agent(
        model=bedrock_model, callback_handler=None, tools=[current_time, use_aws], hooks=[UseAwsInterceptor()]
    )

    return agent
