from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv
import os
import sys

load_dotenv()

SQLALCHEMY_DATABASE_URL = URL.create(
  drivername="postgresql",
  username=os.getenv("DB_USER"),
  password=os.getenv("DB_PASSWORD"),
  host="localhost",
  database=os.getenv("DB_NAME"),
  port=5432
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SQLALCHEMY_DATABASE_URL_TEST = URL.create(
  drivername="postgresql",
  username=os.getenv("DB_USER"),
  password=os.getenv("DB_PASSWORD"),
  host="localhost",
  database=os.getenv("DB_NAME_TEST"),
  port=5432
)

engine_test = create_engine(SQLALCHEMY_DATABASE_URL_TEST)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

Base = declarative_base()

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_session():
    # Check if we're running tests (pytest sets this environment variable)
    if 'pytest' in sys.modules:
        return TestingSessionLocal()
    return SessionLocal()

# Create a global session that will automatically use the correct database
session = get_session()

