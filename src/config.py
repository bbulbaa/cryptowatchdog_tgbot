import os
from dotenv import load_dotenv

# API настройки
COINMARKETCAP_API = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
load_dotenv()

API_KEY = os.getenv("COINMARKETCAP_API_KEY")
TG_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Настройки базы данных
DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "crypto.db")

# Отслеживаемые криптовалюты
TRACKED_COINS = ["SUI", "ETH", "DOGE", "SOL", "BTC"]

# Настройки сбора данных
UPDATE_INTERVAL = 30

# Логи
LOG_FILE = "crypto_bot.log"