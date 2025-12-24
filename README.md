# Strands Agents Playground

## CDK

### Exports

```
export CDK_ACCOUNT_ID=
export CDK_REGION_NAME=
```

## Run the agent with UI

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
hatch run agent_ui
```