# CryptoWatchDog
Система мониторинга криптовалют с Telegram-ботом

## Запуск
1. Зарегистрируйтесь на [CoinMarketCap](https://coinmarketcap.com/api/) для получения API-ключа
2. Создайте бота через [@BotFather](https://t.me/BotFather)
3. Заполните `src/config.py`
4. Установите зависимости: `pip install -r requirements.txt`
5. Запустите сборщик данных: `python src/data_collector.py`
6. Запустите бота: `python src/bot.py`

## Функционал
- Автоматический сбор цен каждые 5 минут
- Хранение данных в SQLite
- Формирование отчетов
- Telegram-бот с командами:
  /start - приветствие
  /prices - текущие цены
  /report - аналитика за 24ч
