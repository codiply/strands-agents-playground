import copy
import os
from typing import Any

from strands.types.tools import ToolResult, ToolUse
from strands_tools.use_aws import TOOL_SPEC as ORIGINAL_TOOL_SPEC
from strands_tools.use_aws import use_aws as original_use_aws

# Make a deep copy of the original TOOL_SPEC.
# Strands Agents expects this to be called TOOL_SPEC within the module
TOOL_SPEC = copy.deepcopy(ORIGINAL_TOOL_SPEC)

# Set a new name for our own implementation
TOOL_SPEC["name"] = "controlled_use_aws"

# Remove the profile_name parameter from the spec
del TOOL_SPEC["inputSchema"]["json"]["properties"]["profile_name"]  # type: ignore


# The environment variable must be set. I let it fail if not.
PROFILE_NAME = os.environ["AGENT_TOOL_USE_AWS_PROFILE_NAME"]


def controlled_use_aws(tool: ToolUse, **kwargs: Any) -> ToolResult:
    tool["input"]["profile_name"] = PROFILE_NAME

    return original_use_aws(tool, **kwargs)
