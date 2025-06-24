from fastapi import FastAPI
from .routers import crypto
from src.config import API_KEY

app = FastAPI(title="CryptoWatchDog API")

app.include_router(crypto.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "CryptoWatchDog API",
        "api_key": API_KEY[-4:] + "..." if API_KEY else "NOT SET"
    }