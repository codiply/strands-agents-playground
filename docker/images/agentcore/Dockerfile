FROM --platform=linux/arm64 python:3.12-slim-bookworm

WORKDIR /app

RUN python -m pip install hatch

COPY pyproject.toml ./
RUN hatch dep show requirements > requirements.txt
RUN python -m pip install -r /app/requirements.txt

COPY src/ ./

ARG AWS_ACCOUNT_ID
ARG AWS_REGION_NAME
ARG AGENT_TOOL_USE_AWS_PROFILE_NAME="strands-playground-tool-use-aws"
ARG AGENT_TOOL_USE_AWS_ROLE_NAME="strands-playground-tool-use-aws"

RUN mkdir /root/.aws/
RUN echo "[profile ${AGENT_TOOL_USE_AWS_PROFILE_NAME}]"                                 >> /root/.aws/config
RUN echo "region=${AWS_REGION_NAME}"                                                    >> /root/.aws/config
RUN echo "role_arn=arn:aws:iam::${AWS_ACCOUNT_ID}:role/${AGENT_TOOL_USE_AWS_ROLE_NAME}" >> /root/.aws/config
# https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/security-credentials-management.html
RUN echo "credential_source=Ec2InstanceMetadata"                                        >> /root/.aws/config

EXPOSE 8080

CMD ["uvicorn", "playground.agentcore:app", "--host", "0.0.0.0", "--port", "8080"]