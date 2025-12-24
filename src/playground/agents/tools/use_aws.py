import copy
import os
from typing import Any

from strands.types.tools import ToolResult, ToolUse
from strands_tools.use_aws import TOOL_SPEC as ORIGINAL_TOOL_SPEC
from strands_tools.use_aws import use_aws as original_use_aws

TOOL_SPEC = copy.deepcopy(ORIGINAL_TOOL_SPEC)

# Remove the profile_name parameter from the spec
del TOOL_SPEC["inputSchema"]["json"]["properties"]["profile_name"]  # type: ignore

PROFILE_NAME_ENV_VARIABLE = "AGENT_TOOL_USE_AWS_PROFILE_NAME"


def use_aws(tool: ToolUse, **kwargs: Any) -> ToolResult:
    if PROFILE_NAME_ENV_VARIABLE in os.environ:
        tool["input"]["profile_name"] = os.environ[PROFILE_NAME_ENV_VARIABLE]
    return original_use_aws(tool, **kwargs)
