from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from chatbot.core.constants import HUGGINGFACEHUB_API_TOKEN
from chatbot.llm_agent.state import AgentState


class BaseNode:
    node_name = ""

    async def invoke_llm(self, chain, inputs, config):
        response = await chain.ainvoke(inputs, config)
        return response

    def get_model(self):
        # model = OpenAI(model="gpt-4o-mini", streaming=True)
        callbacks = [StreamingStdOutCallbackHandler()]

        model = HuggingFaceEndpoint(
            # endpoint_url="http://localhost:8010/",
            repo_id="microsoft/Phi-3-mini-4k-instruct",
            max_new_tokens=512,
            top_k=10,
            top_p=0.95,
            typical_p=0.95,
            temperature=0.01,
            repetition_penalty=1.03,
            callbacks=callbacks,
            streaming=True,
            huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
        )

        return model

    async def execute(self, state: AgentState, config):
        raise NotImplementedError
