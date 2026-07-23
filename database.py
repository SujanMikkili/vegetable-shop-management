"""
Database layer for the Vegetable Shop Management System.

Uses a mysql-connector connection pool so FastAPI's async request
handling never has to wait on a single shared connection.
"""

import mysql.connector
from mysql.connector import pooling

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Your Password",   # <-- set your MySQL password here
    "database": "veg_shop",
}

_pool = pooling.MySQLConnectionPool(
    pool_name="veg_shop_pool",
    pool_size=5,
    **DB_CONFIG,
)


def execute_query(query: str, params: tuple | None = None, fetch: bool = False):
    """
    Run a query against MySQL.

    fetch=True  -> SELECT, returns list[dict]
    fetch=False -> INSERT/UPDATE/DELETE, commits and returns None
    """
    conn = _pool.get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        if fetch:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = None
        cursor.close()
        return result
    except mysql.connector.Error as err:
        raise Exception(f"Database error: {err}")
    finally:
        conn.close()
