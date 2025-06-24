from fastapi import HTTPException, Header
from .. import config

def get_api_key(x_api_key: str = Header(...)):
    """Простая проверка API ключа"""
    if x_api_key != config.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return x_api_key