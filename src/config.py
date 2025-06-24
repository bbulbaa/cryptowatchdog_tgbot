import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from pathlib import Path

# API настройки
COINMARKETCAP_API = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

API_KEY = os.getenv("COINMARKETCAP_API_KEY")
TG_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Настройки базы данных
DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "crypto.db")

# Отслеживаемые криптовалюты
TRACKED_COINS = ["SUI", "ETH", "DOGE", "SOL", "BTC"]

# Настройки сбора данных
UPDATE_INTERVAL = 300  # 5 минут

# Логи
LOG_DIR = "logs"  # Добавляем директорию для логов
LOG_FILE = os.path.join(LOG_DIR, "crypto_bot.log")  # Изменяем путь

def setup_logging():
    # Создаем директорию для логов если нужно
    os.makedirs(LOG_DIR, exist_ok=True)
    
    handler = RotatingFileHandler(
        LOG_FILE, 
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5
    )
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)
    
    return handler

# Инициализация логирования
handler = setup_logging()