import sqlite3
from pathlib import Path
from datetime import datetime

def init_db(db_file: Path):
    """Initialize SQLite database"""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            product TEXT NOT NULL,
            amount REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_order(db_file: Path, customer_name: str, product: str, amount: float) -> int:
    """Add new order to database"""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (customer_name, product, amount, created_at) VALUES (?, ?, ?, ?)",
        (customer_name, product, amount, datetime.now().isoformat())
    )
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return order_id

def list_orders(db_file: Path, status: str = None) -> list:
    """List all orders, optionally filtered by status"""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    if status:
        cursor.execute(
            "SELECT id, customer_name, product, amount, status, created_at FROM orders WHERE status = ?",
            (status,)
        )
    else:
        cursor.execute("SELECT id, customer_name, product, amount, status, created_at FROM orders")
    
    orders = cursor.fetchall()
    conn.close()
    return orders

def update_order_status(db_file: Path, order_id: int, status: str):
    """Update order status"""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
    conn.commit()
    conn.close()
