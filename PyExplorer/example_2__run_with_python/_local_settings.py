"""
ВНИМНИЕ!!!
Использую .env - чтобы скрыть мой личный пароль!
"""

from dotenv import load_dotenv   # pip install python-dotenv
import os

load_dotenv()

postgres_config = {
    "dbname": 'java_rush',
    "user":'postgres',
    "password": "1",
    "host": "localhost",
    "port": "5432"
}

mysql_config = {
    "host": "localhost",
    "user": "root",
    "password": os.getenv("MYSQL_PASSWORD")
}