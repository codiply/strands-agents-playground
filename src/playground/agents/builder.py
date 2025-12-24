from strands import Agent
from strands.models import BedrockModel
from strands_tools import current_time

from playground.agents.tools import use_aws as use_aws

MODEL_ID = "eu.amazon.nova-micro-v1:0"
# MODEL_ID="eu.amazon.nova-pro-v1:0"


def build_agent() -> Agent:
    bedrock_model = BedrockModel(
        model_id=MODEL_ID,
        temperature=0.3,
        # streaming=True,
    )

    agent = Agent(model=bedrock_model, callback_handler=None, tools=[current_time, use_aws])

    return agent
