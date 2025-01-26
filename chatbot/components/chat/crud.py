from uuid import UUID
from sqlalchemy.orm import Session

from chatbot.components.chat.enums import QueryResponseStatus
from chatbot.components.chat.models import QueryResponse, UserQuery
from chatbot.components.chat.schemas import ChatSchema
from chatbot.components.user.models import User


class ChatCrud:
    def __init__(self, user: User, db: Session):
        self.user = user
        self.db = db

    def create_user_query(self, query: str) -> UserQuery:
        user_query = UserQuery(user_id=self.user.id, query=query)

        self.db.add(user_query)
        self.db.flush()
        self.db.refresh(user_query)

        return user_query

    def get_user_query(self, query_id: UUID) -> UserQuery | None:
        user_query = (
            self.db.query(UserQuery)
            .filter(
                UserQuery.user_id == self.user.id,
                UserQuery.query_id == query_id,
                UserQuery.is_deleted == False,
            )
            .first()
        )

        return user_query

    def get_latest_query(self) -> UserQuery | None:
        user_query = (
            self.db.query(UserQuery)
            .filter(
                UserQuery.user_id == self.user.id,
                UserQuery.is_deleted == False,
            )
            .order_by(UserQuery.created_at.desc())
            .first()
        )

        return user_query

    def create_query_response(self, query_id: int, response: str) -> UserQuery:
        query_response = QueryResponse(query_id=query_id, response=response)

        self.db.add(query_response)
        self.db.flush()
        self.db.refresh(query_response)

        return query_response

    def get_query_response(self, query_obj: UserQuery) -> QueryResponse | None:
        query_response = (
            self.db.query(QueryResponse)
            .filter(QueryResponse.query_id == query_obj.id)
            .order_by(QueryResponse.created_at.desc())
            .first()
        )

        return query_response

    def update_response_status(
        self, response_obj: QueryResponse, status: QueryResponseStatus
    ):
        response_obj = self.db.merge(response_obj)

        response_obj.status = status

        self.db.flush()
        self.db.refresh(response_obj)

        return response_obj

    def update_response_failed(self, response_obj: QueryResponse, error: Exception):
        response_obj = self.db.merge(response_obj)

        response_obj.status = QueryResponseStatus.FAILED
        response_obj.failure_reason = {"error": str(error)}

        self.db.flush()
        self.db.refresh(response_obj)

        return response_obj

    def get_chat_history(
        self,
        count: int | None = None,
        last_query_id: int | None = None,
    ) -> tuple[list[ChatSchema], bool]:
        if not count:
            count = 10

        query = self.db.query(UserQuery).filter(
            UserQuery.user_id == self.user.id,
            UserQuery.is_deleted == False,
        )

        if last_query_id:
            query = query.filter(UserQuery.id < last_query_id)

        queries = query.order_by(UserQuery.id.desc()).limit(count + 1).all()
        is_last_page = len(queries) <= count

        if not is_last_page:
            queries = queries[:-1]

        query_ids = [q.id for q in queries]
        latest_responses = (
            self.db.query(QueryResponse)
            .filter(QueryResponse.query_id.in_(query_ids))
            .order_by(QueryResponse.query_id, QueryResponse.id.desc())
            .distinct(QueryResponse.query_id)
            .all()
        )

        response_dict = {response.query_id: response for response in latest_responses}

        chat_history = []

        for query in queries:
            response_text = None
            response_id = None
            status = QueryResponseStatus.FAILED

            response = response_dict.get(query.id)
            if response:
                response_text = response.response
                response_id = response.response_id
                status = response.response_status

            chat_history.append(
                {
                    "query": query.query,
                    "query_id": query.query_id,
                    "response": response_text,
                    "response_id": response_id,
                    "status": status,
                }
            )

        return chat_history, is_last_page
