import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
import time

load_dotenv()

MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
MYSQL_DB = os.getenv('MYSQL_DB', 'optimizer_db')
MYSQL_PORT = os.getenv('MYSQL_PORT', '3306')

DB_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

engine = None
for i in range(5):
    try:
        engine = create_engine(DB_URL, pool_pre_ping=True)
        conn = engine.connect()
        conn.close()
        break
    except OperationalError as e:
        print(f"DB connection failed, retrying... ({i+1}/5)")
        time.sleep(2)
else:
    raise Exception("Could not connect to the database after 5 attempts.")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_engine():
    return engine

def get_session():
    return SessionLocal() 