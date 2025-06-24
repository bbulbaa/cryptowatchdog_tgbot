import sqlite3
import os
from config import DB_PATH, DB_DIR

def init_db():
    """Инициализация базы данных"""
    try:
        # Создаем директорию если не существует
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Создаем таблицу
        c.execute('''
            CREATE TABLE IF NOT EXISTS prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                coin TEXT NOT NULL,
                price REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Создаем индекс для быстрого поиска
        c.execute('''
            CREATE INDEX IF NOT EXISTS idx_coin_timestamp 
            ON prices (coin, timestamp DESC)
        ''')
        
        conn.commit()
        print(f"База данных инициализирована: {DB_PATH}")
    except sqlite3.Error as e:
        print(f"Ошибка инициализации БД: {str(e)}")
    finally:
        if conn:
            conn.close()

def save_price(coin: str, price: float):
    """Сохранение цены в БД"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            INSERT INTO prices (coin, price) 
            VALUES (?, ?)
        """, (coin, price))
        conn.commit()
    except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                logger.warning("БД заблокирована, повтор попытки...")
                time.sleep(0.5)
                save_price(coin, price)  # Рекурсивный повтор
            else:
                logger.error(f"Ошибка БД: {str(e)}")
    except sqlite3.Error as e:
        print(f"Ошибка сохранения данных: {str(e)}")
    finally:
        if conn:
            conn.close()