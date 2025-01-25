from fastapi import APIRouter


from chatbot.api.v1.auth.routes import api_router as auth_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["auth"])
