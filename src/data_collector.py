import httpx
import time
import logging
from .database import save_price
from .config import *
from .datetime import datetime, timezone

logger = logging.getLogger(__name__)

LAST_UPDATE_TIME = None

async def fetch_crypto_prices():
    """Асинхронный запрос цен криптовалют с CoinMarketCap"""
    global LAST_UPDATE_TIME  # Важно!
    
    headers = {"X-CMC_PRO_API_KEY": API_KEY}  # Добавлено
    
    async with httpx.AsyncClient() as client:
        while True:
            try:
                response = await client.get(
                    COINMARKETCAP_API,
                    headers=headers,
                    params={"symbol": ",".join(TRACKED_COINS), "convert": "USD"},
                    timeout=10
                )
                data = response.json()
            
                saved_count = 0
                crypto_data = data.get("data", {})
                
                for symbol in TRACKED_COINS:
                    coin_data = crypto_data.get(symbol)
                    if coin_data:
                        price = coin_data["quote"]["USD"]["price"]
                        save_price(symbol, price)
                        saved_count += 1
                        logger.info(f"Сохранено {symbol}: ${price:.4f}")
                    else:
                        logger.warning(f"Монета {symbol} не найдена в ответе API")
                
                logger.info(f"Успешно сохранено {saved_count}/{len(TRACKED_COINS)} монет")
                LAST_UPDATE_TIME = datetime.now(timezone.utc)
                
            except Exception as e:
                logger.error(f"Ошибка: {str(e)}")
            
            await asyncio.sleep(UPDATE_INTERVAL)