from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# Create an engine
# engine = create_engine('sqlite:///site.db')

# Reflect the existing database schema
# Base = automap_base()
# Base.prepare(autoload_with=engine)

# Access the generated model classes
# mytable = Base.classes.basic_info


def custom_api(db, data):
    SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{db["db_user"]}:{db["db_password"]}@{db["db_host"]}:{db["db_port"]}/{db["db_name"]}'
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base = automap_base()
    Base.prepare(autoload_with=engine)
    mytable = Base.classes.basic_info
    with Session(engine) as session:
        queryset = session.query(mytable).all()
        obj=queryset[0]
        # engine.dispose()
        return obj
