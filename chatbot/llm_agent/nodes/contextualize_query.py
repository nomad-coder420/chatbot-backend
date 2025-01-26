from langchain.prompts import PromptTemplate

from chatbot.llm_agent.constants import NodeName
from chatbot.llm_agent.nodes.base import BaseNode
from chatbot.llm_agent.state import AgentState


class ContextualizeQueryNode(BaseNode):
    node_name = NodeName.CONTEXTUALIZE_QUERY.value

    async def execute(self, state: AgentState, config):
        query = state["query"]
        chat_history = state["chat_history"]

        prompt = PromptTemplate.from_template(
            "Using history: {chat_history}, answer the query: {query} in 200 words or less. Dont tell me steps of how you did it, just give me the answer."
        )

        model = self.get_model()
        chain = prompt | model

        response = await self.invoke_llm(
            chain, {"query": query, "chat_history": chat_history}, config
        )

        return {"refined_query": "New refined query"}
