from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:nanox@localhost/api_studio"
# SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:Mani_123@localhost:3306/testdb"

SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://microapi:M!cr0ap!*C$E*@localhost:5432/apicloud'
#SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://postgres:postgres@192.168.1.37:5432/MainApp'
# SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://postgres:BXz0cNwxSwzqW1wn@db.kfysllxtigevtikqbpvt.supabase.co:5432/postgres'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
