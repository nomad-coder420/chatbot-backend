from fastapi import APIRouter, Depends

api_router = APIRouter()

@api_router.post("/login")
def login(username: str, password: str):
    print("Perform login here...")
    return {"access_token": "token", "token_type": "bearer"}
