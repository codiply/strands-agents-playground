import json
from typing import List

import gradio as gr
from loguru import logger
from pydantic import BaseModel, Field
from strands import Agent
from strands.hooks.events import MessageAddedEvent
from strands.types.content import Message


class UiState(BaseModel):
    all_messages: List[Message] = Field(default_factory=list)

    def pretty_all_messages(self) -> str:
        # return "\n".join([json.dumps(m, indent=4) for m in self.all_messages])
        return json.dumps(self.all_messages, indent=4)


def build_agent_chat_function(agent: Agent, ui_state: UiState):
    def chat_function(message, _history):
        logger.info("Received message '{message}'", message=message)

        if not message:
            return "Please type a message"

        result = agent(message)

        return str(result), ui_state.pretty_all_messages()

    return chat_function


def build_ui(agent: Agent) -> gr.ChatInterface:
    ui_state = UiState()

    agent.hooks.add_callback(MessageAddedEvent, lambda event: ui_state.all_messages.append(event.message))

    all_messages_block = gr.Code(language="json", render=False, wrap_lines=True)

    with gr.Blocks() as ui:
        with gr.Tab("Chat Interface"):
            gr.ChatInterface(
                fn=build_agent_chat_function(agent, ui_state),
                title="Agent Chat",
                additional_outputs=[all_messages_block],
            )
        with gr.Tab("Internal Dialog"):
            all_messages_block.render()

    return ui
