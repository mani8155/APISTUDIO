from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy import create_engine, Column, DateTime, Text, Integer
from urllib.parse import quote_plus

Base = declarative_base()

class Test(Base):
    """
    SQLAlchemy model representing the 'developer_menu' table.

    Attributes:
        id (int): The primary key for the table.
        created_at (DateTime): The column representing the creation timestamp.
    """

    __tablename__ = 'developer_menu'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)

def custom_api(db, data):
    """
    Custom API function for creating a SQLAlchemy engine.

    Args:
        db (dict): A dictionary containing database connection details.
        data: Additional data (not used in this function).

    Returns:
        str: A message indicating whether the engine was created successfully or not.

    Example Usage:
        db = {
            'db_user': 'username',
            'db_password': 'password',
            'db_host': '127.0.0.1',
            'db_port': '3306',
            'db_name': 'database_name'
        }
        result = custom_api(db, data)

    Note:
        Uncomment the code inside the function to perform additional operations such as querying the database.
    """

    # Encoding the database password
    db_password_encoded = quote_plus('Nanox@cse#@!2428')

    # mysql_db_url = f"mysql+mysqlconnector://nano:{db_password_encoded}@192.168.1.100:3306/etltestdb"
    # mysql_db_url = f"mysql+pymysql://root:{db_password_encoded}@127.0.0.1:3306/nanox_books"
    # Constructing the database URL    
    SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{db["db_user"]}:{db["db_password"]}@{db["db_host"]}:{db["db_port"]}/{db["db_name"]}'

    # Creating the SQLAlchemy engine
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    if engine:
        return data
    else:
        return 'Engine not created'

    # Uncomment the following code to perform additional operations with the engine
    # with Session(engine) as session:
    # 	single_row = session.query(Test).first()
    # 	myvar = single_row.__dict__
    # 	return myvar