from typing import Any
from langchain.chains.llm import LLMChain
from langchain_google_vertexai import VertexAI
from langchain_core.callbacks.manager import adispatch_custom_event

from chatbot.llm_agent.state import AgentState


class BaseNode:
    node_name = ""
    direct_stream_llm_response = False

    async def invoke_llm(self, chain: LLMChain, inputs, config) -> Any:
        if self.direct_stream_llm_response:
            response = ""
            async for chunk in chain.astream(inputs, config):
                await adispatch_custom_event(
                    "on_chunk_stream",
                    {
                        "chunk": chunk,
                        "direct_stream_llm_response": True,
                    },
                    config=config,
                )
                print("chunkkkk", type(chunk), chunk, end="\n\n\n")

                response += chunk

            return response
        else:
            response = await chain.ainvoke(inputs, config)
            return response

    def get_model(self):
        init_params = {
            "project": "artisan-assignment-chatbot",
            "model_name": "gemini-1.5-flash-001",
            "location": "us-west1",
            "temperature": 0,
            "top_p": 0,
            "streaming": True,
        }

        model = VertexAI(**init_params)
        return model

    def get_parser(self):
        return

    async def execute(self, state: AgentState, config):
        raise NotImplementedError
