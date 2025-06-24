from fastapi import APIRouter, Depends
from pydantic import BaseModel
from .. import dependencies
from src.analytics import get_coin_history  # Импорт из вашего кода

router = APIRouter()

class PriceResponse(BaseModel):
    coin: str
    price: float
    timestamp: str

@router.get("/prices", response_model=list[PriceResponse])
async def get_prices(api_key: str = Depends(dependencies.get_api_key)):
    """Получение текущих цен"""
    results = []
    for coin in TRACKED_COINS:
        history = get_coin_history(coin, limit=1)
        if history:
            price, timestamp = history[0]
            results.append(PriceResponse(
                coin=coin,
                price=price,
                timestamp=timestamp
            ))
    return results