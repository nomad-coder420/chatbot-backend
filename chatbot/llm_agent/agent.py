import os
from threading import Lock
from langgraph.graph import StateGraph, END

from chatbot.llm_agent.constants import NodeName
from chatbot.llm_agent.nodes.contextualize_query import ContextualizeQueryNode
from chatbot.llm_agent.state import AgentState

agent = None


def get_agent():
    global agent

    if agent:
        return agent

    graph = StateGraph(AgentState)
    agent = graph.compile()


class LlmAgent:
    _instance = None
    _lock = Lock()
    _agent = None

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
            return cls._instance

    @classmethod
    def get_agent(cls):
        if not cls._instance:
            raise Exception("Agent not initialized")

        if cls._agent:
            return cls._agent

        cls._agent = cls.create_agent()
        return cls._agent

    @classmethod
    def create_agent(self):
        print("Creating agent")

        graph = StateGraph(AgentState)

        graph.add_node(
            NodeName.CONTEXTUALIZE_QUERY.value, ContextualizeQueryNode().execute
        )

        graph.set_entry_point(NodeName.CONTEXTUALIZE_QUERY.value)
        graph.add_edge(NodeName.CONTEXTUALIZE_QUERY.value, END)

        agent = graph.compile()
        curr_dir = os.getcwd()
        agent.get_graph().draw_mermaid_png(output_file_path=f"{curr_dir}/chatbot/llm_agent/agent.png")

        return agent
