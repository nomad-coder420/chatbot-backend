from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from chatbot.api.v1.router import router as v1_router
from chatbot.middlewares.exceptions import ExceptionMiddleware

app = FastAPI()


app.include_router(v1_router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This now allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ExceptionMiddleware)
