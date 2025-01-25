from fastapi import APIRouter


from chatbot.api.v1.routes import api_router as app_router

router = APIRouter()

router.include_router(app_router)
