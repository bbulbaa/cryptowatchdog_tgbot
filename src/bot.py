import os
import threading
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import TG_TOKEN, TRACKED_COINS
from analytics import get_coin_history, generate_report
from database import init_db
from data_collector import fetch_crypto_prices
import logging

logging.getLogger("httpx").setLevel(logging.WARNING) # чтобы не шумело 
def start_data_collector():
    """Запуск сбора данных в фоновом режиме"""
    fetch_crypto_prices()
    print("Первоначальные данные успешно загружены!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 CryptoWatchDog активен!\n\n"
        "Доступные команды:\n"
        "/prices - текущие цены криптовалют\n"
        "/report - аналитический отчет за 24 часа"
    )

async def prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        msg = "📈 Последние цены:\n\n"
        
        for coin in TRACKED_COINS:
            history = get_coin_history(coin, limit=1)
            if history:
                last_price = history[0][0]
                msg += f"{coin}: ${last_price:.4f}\n"
            else:
                msg += f"{coin}: данные отсутствуют\n"
        
        await update.message.reply_text(msg)
    except Exception as e:
        await update.message.reply_text(f"🚨 Ошибка: {str(e)}")
        logger.error(f"Ошибка в /prices: {str(e)}")

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        df = generate_report()
        if df.empty:
            await update.message.reply_text("📊 Данные для отчета еще не собраны")
            return
            
        await update.message.reply_text(
            f"📊 Отчет за 24 часа:\n\n"
            f"```\n{df.to_string(index=False)}\n```",
            parse_mode="Markdown"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка генерации отчета: {str(e)}")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from data_collector import LAST_UPDATE_TIME  # Добавить глобальную переменную в data_collector
    
    status_msg = (
        f"🟢 Бот активен\n"
        f"Последнее обновление: {LAST_UPDATE_TIME.strftime('%H:%M:%S') if LAST_UPDATE_TIME else 'никогда'}\n"
        f"Монет в отслеживании: {len(TRACKED_COINS)}"
    )
    await update.message.reply_text(status_msg)

def main():
    # Инициализация БД
    init_db()
    
    # Запускаем сбор данных сразу при старте в отдельном потоке
    data_thread = threading.Thread(target=start_data_collector)
    data_thread.daemon = True  # Демонизируем поток
    data_thread.start()
    
    # Создаем приложение
    application = Application.builder().token(TG_TOKEN).build()
    
    # Регистрируем обработчики команд
    command_handlers = [
        CommandHandler("start", start),
        CommandHandler("prices", prices),
        CommandHandler("report", report)
    ]
    
    for handler in command_handlers:
        application.add_handler(handler)
    
    # Запускаем бота
    print("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()