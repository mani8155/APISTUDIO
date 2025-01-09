from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


#SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://postgres:postgres@localhost:5432/MainApp'
SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://microapi:M!cr0ap!*C$E*@localhost:5432/apicloud'
#SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://postgres:BXz0cNwxSwzqW1wn@db.kfysllxtigevtikqbpvt.supabase.co:5432/postgres'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
