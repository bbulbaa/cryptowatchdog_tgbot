import requests
import time
import logging
from database import save_price
from config import COINMARKETCAP_API, API_KEY, TRACKED_COINS, UPDATE_INTERVAL, LOG_FILE
from datetime import datetime, timezone

LAST_UPDATE_TIME = None

# Настройка логирования
logger = logging.getLogger("DATA_COLLECTOR")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(LOG_FILE)  # <--- Пишем в файл
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def fetch_crypto_prices():
    """Запрос цен криптовалют с CoinMarketCap"""
    headers = {
        "X-CMC_PRO_API_KEY": API_KEY,
        "Accept": "application/json"
    }
    try:
        while True:
            response = requests.get(
                COINMARKETCAP_API,
                headers=headers,
                 params={"limit": 50, "convert": "USD"},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            print(data)
            
            saved_count = 0
            for coin in data.get("data", []):
                symbol = coin["symbol"]
                if symbol in TRACKED_COINS:
                    price = coin["quote"]["USD"]["price"]
                    save_price(symbol, price)
                    saved_count += 1
                    logger.info(f"Сохранено {symbol}: ${price:.4f}")
            
            logger.info(f"Успешно сохранено {saved_count}/{len(TRACKED_COINS)} монет")
            return saved_count
            LAST_UPDATE_TIME = datetime.now(timezone)

            time.sleep(UPDATE_INTERVAL)
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка API: {str(e)}")
        return 0
    except (KeyError, ValueError) as e:
        logger.error(f"Ошибка обработки данных: {str(e)}")
        return 0