import os
from typing import Any

from strands.hooks import BeforeToolCallEvent, HookProvider, HookRegistry
from strands_tools.use_aws import TOOL_SPEC

TOOL_NAME = TOOL_SPEC["name"]

PROFILE_NAME_ENV_VARIABLE = "AGENT_TOOL_USE_AWS_PROFILE_NAME"


class UseAwsInterceptor(HookProvider):
    def register_hooks(self, registry: HookRegistry, **kwargs: Any) -> None:
        registry.add_callback(BeforeToolCallEvent, self.intercept_tool)

    def intercept_tool(self, event: BeforeToolCallEvent) -> None:
        if event.tool_use["name"] == TOOL_NAME:
            if PROFILE_NAME_ENV_VARIABLE in os.environ:
                event.tool_use["input"]["profile_name"] = os.environ[PROFILE_NAME_ENV_VARIABLE]
                event.tool_use["name"] = "safe_tool"
