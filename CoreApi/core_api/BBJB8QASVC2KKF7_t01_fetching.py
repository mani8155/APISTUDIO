from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy import create_engine, Column, DateTime, Text, Integer
from urllib.parse import quote_plus

# Create an engine
# engine = create_engine('sqlite:///site.db')

# Reflect the existing database schema
# Base = automap_base()
# Base.prepare(autoload_with=engine)

# Access the generated model classes
# mytable = Base.classes.basic_info

Base = declarative_base()

class Test(Base):
    __tablename__ = 'developer_menu'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)


def custom_api(db, data):
    db_password_encoded=quote_plus('Nanox@cse#@!2428')
    mysql_db_url = f"mysql+pymysql://root:{db_password_encoded}@127.0.0.1:3306/nanox_books"
    # SQLALCHEMY_DATABASE_URL = f'mysql+py://{db["db_user"]}:{db["db_password"]}@{db["db_host"]}:{db["db_port"]}/{db["db_name"]}'
    # mysql_db_url = f"mysql+mysqlconnector://nano:{db_password_encoded}@192.168.1.100:3306/etltestdb"
    engine = create_engine(mysql_db_url)


    with Session(engine) as session:
        # queryset = session.query(Test).all()
        # myvar = [i.__dict__ for i in queryset]

        # return myvar

        single_row = session.query(Test).fetchone()
        myvar = single_row.__dict__ 
        # engine.dispose()
        return myvar




