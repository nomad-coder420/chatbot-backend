from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from chatbot.components.chat.enums import QueryResponseStatus
from chatbot.components.chat.models import QueryResponse
from chatbot.components.user.models import User


class AsyncChatCrud:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_response_obj(self, response_id: UUID) -> QueryResponse:
        query_result = await self.db.execute(
            select(QueryResponse).where(QueryResponse.response_id == response_id)
        )

        response_obj = query_result.scalar_one()

        return response_obj

    async def update_response_status(
        self, response_obj: QueryResponse, status: QueryResponseStatus
    ):
        response_obj = await self.db.merge(response_obj)

        response_obj.response_status = status

        await self.db.commit()
        await self.db.refresh(response_obj)

        return response_obj

    async def update_response_failed(
        self, response_obj: QueryResponse, error: Exception
    ):
        response_obj = await self.db.merge(response_obj)

        response_obj.response_status = QueryResponseStatus.FAILED
        response_obj.failure_reason = {"error": str(error)}

        await self.db.commit()
        await self.db.refresh(response_obj)

        return response_obj

    async def update_query_response(self, response_obj: QueryResponse, response: str):
        response_obj = await self.db.merge(response_obj)

        response_obj.response += response

        await self.db.commit()
        await self.db.refresh(response_obj)

        return response_obj
