from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from chatbot.llm_agent.constants import NodeName
from chatbot.llm_agent.nodes.base import BaseNode
from chatbot.llm_agent.parsers import ContextualiseParser
from chatbot.llm_agent.state import AgentState


system_prompt = """You are a Query Contextualizer, skilled at reformulating user queries into standalone questions.  

Given a chat history and the latest user message, interpret and refine the query to make it self-contained and \
understandable without any prior context. Always prioritize the user's latest query and only reference chat history \
if absolutely necessary to provide clarity.  

### Instructions:  
- Do NOT answer the question or infer things.  
- Ensure the reformulated query is concise, to the point, and based on the user's latest message.  
- If no context from the history is required, simply return the latest query as is.  
- Avoid including unnecessary details or previous queries in the output.  

Respond strictly in this format:  
```json
{{
    "contextualised_query": "<reformulated query/same query>"
}}

{format_instructions}"""


class ContextualizeQueryNode(BaseNode):
    node_name = NodeName.CONTEXTUALIZE_QUERY.value

    async def execute(self, state: AgentState, config):
        query = state["query"]
        chat_history = state["chat_history"]

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        model = self.get_model()
        parser = self.get_parser()
        chain = prompt | model | parser

        response = await self.invoke_llm(
            chain,
            {
                "input": query,
                "chat_history": chat_history,
                "format_instructions": parser.get_format_instructions(),
            },
            config,
        )

        print(response)

        return {"contextualised_query": response.get("contextualised_query")}

    def get_parser(self):
        return JsonOutputParser(pydantic_object=ContextualiseParser)
