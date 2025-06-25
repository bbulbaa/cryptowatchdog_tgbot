# 🚀 CryptoWatchDog - Система мониторинга криптовалют

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Telegram](https://img.shields.io/badge/Telegram-Bot-green)
![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-yellowgreen)

Система мониторинга криптовалют с отслеживанием в реальном времени, аналитикой и отчетностью. Построена на современном Python-стеке.

## ✨ Функциональные возможности
- Отслеживание цен в реальном времени для 5+ криптовалют
- Автоматический сбор данных каждые 5 минут
- Telegram-бот с командами:
  - `/prices` - Текущие рыночные цены
  - `/report` - Аналитический отчет за 24 часа
  - `/status` - Проверка состояния системы
- REST API для интеграции
- База данных SQLite с оптимизированными запросами
- Базовое логирование в файл

## 🛠 Технологический стек
- **Ядро**: Python 3.10+
- **Telegram**: python-telegram-bot
- **API**: FastAPI + Uvicorn
- **Данные**: Pandas + SQLAlchemy
- **БД**: SQLite (Локальное хранилище для демо)
- **Сетевое взаимодействие**: HTTPX (асинхронный)

## 🚀 Быстрый старт

### Предварительные требования
- Python 3.10+
- Токен Telegram-бота ([получить здесь](https://t.me/BotFather))
- API-ключ CoinMarketCap ([получить здесь](https://coinmarketcap.com/api/))

### Установка
```bash
git clone https://github.com/bbulbaa/cryptowatchdog_tgbot/
cd cryptowatchdog
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

pip install -r requirements.txt
