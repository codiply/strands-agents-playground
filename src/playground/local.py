from playground.agents.builder import build_agent
from playground.ui.chat import build_ui

agent = build_agent()

ui = build_ui(agent)

ui.launch()
