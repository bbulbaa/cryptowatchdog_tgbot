import logging
import os
import sqlite3
import pandas as pd
from datetime import datetime, timedelta, timezone
from .config import *

logger = logging.getLogger(__name__)

def generate_report():
    """Генерация аналитического отчета"""
    try:
        conn = sqlite3.connect(DB_PATH)
        
        # Рассчитываем временной диапазон
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(days=1)
        
        query = """
            SELECT 
                coin,
                MAX(timestamp) as last_update,
                ROUND(AVG(price), 4) as avg_price,
                ROUND(MAX(price) - MIN(price), 4) as volatility,
                ROUND((MAX(price) - MIN(price)) / AVG(price) * 100, 2) as volatility_percent
            FROM prices
            WHERE timestamp BETWEEN ? AND ?
            GROUP BY coin
        """
        
        df = pd.read_sql_query(query, conn, params=(start_time.isoformat(), end_time.isoformat()))  # Защита от SQLi
        
        # Создаем директорию для отчетов если нужно
        os.makedirs("reports", exist_ok=True)
        
        # Возвращаем DataFrame даже если он пустой
        return df
        
    except sqlite3.Error as e:
        raise Exception(f"Database error: {str(e)}")
    finally:
        if conn:
            conn.close()

def get_coin_history(coin: str, limit: int = 24):
    """Получение истории цен для монеты"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            SELECT price, timestamp 
            FROM prices 
            WHERE coin = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (coin, limit))
        return c.fetchall()
    except sqlite3.Error:
        return None
    finally:
        if conn:
            conn.close()