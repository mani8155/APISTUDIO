from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# Create an engine
# engine = create_engine('sqlite:///site.db')

# Reflect the existing database schema
# Base = automap_base()
# Base.prepare(autoload_with=engine)

# Access the generated model classes
# mytable = Base.classes.basic_info


def custom_api(db, data):
    db_password_encoded=quote_plus('Nanox@cse#@!2428')
    # mysql_db_url = f"mysql+pymysql://root:{db_password_encoded}@127.0.0.1:3306/nanox_books"
    SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{db["db_user"]}:{db["db_password"]}@{db["db_host"]}:{db["db_port"]}/{db["db_name"]}'
    # mysql_db_url = f"mysql+mysqlconnector://nano:{db_password_encoded}@192.168.1.100:3306/etltestdb"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    if engine:
        return {'message':'created'}
    else:
        return {'engine': 'engine'}

    # Base = automap_base()
    # Base.prepare(autoload_with=engine)
    # mytable = Base.classes.basic_info
    # with Session(engine) as session:
    #     queryset = session.query(mytable).all()
    #     obj=queryset[0]
    #     # engine.dispose()
    #     return obj
