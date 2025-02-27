import mysql.connector
from config import Config

try:
    conn = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB,
        port=Config.MYSQL_PORT
    )
    print("Successfully connected to Railway MySQL!")
    conn.close()
except Exception as e:
    print(f" Connection failed: {e}")
