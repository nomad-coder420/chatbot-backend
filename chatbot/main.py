from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from chatbot.database.session import async_engine
from chatbot.core.models import Base
from chatbot.api.v1.router import router as v1_router
from chatbot.middlewares.db_session import DBSessionMiddleware
from chatbot.middlewares.exceptions import ExceptionMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Sync db to latest revision on startup
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield  # Keep the application running


app = FastAPI(lifespan=lifespan)


app.include_router(v1_router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This now allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(DBSessionMiddleware)
app.add_middleware(ExceptionMiddleware)
