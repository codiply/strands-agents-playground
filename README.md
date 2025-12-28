# Strands Agents Playground

## CDK

### Exports

```
export AWS_ACCOUNT_ID=
export AWS_REGION_NAME=
```

### Base stack

If you only want to run the agent locally, create only the resources in the base stack

```
hatch run cdk:run deploy '*-base'
```

### All stacks

```
hatch run cdk:run deploy --all
```

### Destroy all stacks

```
hatch run cdk:run destroy --all
```

## Run the agent locally with UI

Add a profile in `~/.aws/config`

```
[profile strands-playground-tool-use-aws]
region =
role_arn = 
source_profile = 
```

```
export AGENT_TOOL_USE_AWS_PROFILE_NAME=strands-playground-tool-use-aws
```

```
hatch run agent_with_ui
```

## Test AgentCore locally

Build docker image with

```
hatch run compose build
```

Run the image with

```
hatch run compose up -d
```

(use `hatch run compose down` to stop the container)

Test with

```
curl http://localhost:8080/ping
```

and

```
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{
    "input": {"prompt": "How many S3 buckets do I have?"}
  }'
```