from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{settings.database_username}:{
    settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# The dependency. Not: The is what talks to the databases SessionLocal(), referance database.py
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# settings connection to postgres
# THIS IS NO LONGER IN USE. AM USING SQLALCHEMY INSTEAL. SO I COMMENTED IT
'''
while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi",
                                user="postgres", password="ACCESS", port="5432", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull")
        break
    except Exception as error:
        print(f"Connectiong to database failed: Error is:  {error}")
        time.sleep(3)
'''
