from pydantic import BaseModel, Field


class ContextualiseParser(BaseModel):
    contextualised_query: str = Field(
        description="Reformulated contextualised query if history required else same user query"
    )
