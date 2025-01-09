from urllib.parse import quote_plus

import requests
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base, Session


# def custom_api(db, data):
#     password_encoded = quote_plus(db["db_password"])
#     mssql_connection = f'{db["db_engine"]}+pymssql://{db["db_user"]}:{password_encoded}@{db["db_host"]}:{db["db_port"]}/{db["db_name"]}'
#     mssql_engine = create_engine(mssql_connection)
#     Base = declarative_base()



#     class ErpItemTransactionBcr(Base):
#         __tablename__ = 'spt_monitor'

#         id = Column(Integer, primary_key=True)
#         lastrun = Column(DateTime)
#         cpu_busy = Column(Integer)
#         io_busy = Column(Integer)
#         idle = Column(Integer)
#         pack_received = Column(Integer)
#         pack_sent = Column(Integer)
#         connections = Column(Integer)
#         pack_errors = Column(Integer)
#         total_read = Column(Integer)
#         total_write = Column(Integer)
#         total_errors = Column(Integer)

      

#     with Session(mssql_engine) as mssql_db:
#         obj = mssql_db.query(ErpItemTransactionBcr).filter(ErpItemTransactionBcr.cpu_busy == 23).first()
    
#         return {"success": obj}


def custom_api(db, data):
    password_encoded = quote_plus(db["db_password"])
    mssql_connection = f'{db["db_engine"]}+pymssql://{db["db_user"]}:{password_encoded}@{db["db_host"]}:{db["db_port"]}/{db["db_name"]}'
    mssql_engine = create_engine(mssql_connection)
    Base = declarative_base()

    class ErpItemTransactionBcr(Base):
        __tablename__ = 'spt_monitor'

        # Modify the class attributes to match your actual table schema
        lastrun = Column(DateTime)
        cpu_busy = Column(Integer)
        io_busy = Column(Integer)
        idle = Column(Integer)
        pack_received = Column(Integer)
        pack_sent = Column(Integer)
        connections = Column(Integer)
        pack_errors = Column(Integer)
        total_read = Column(Integer)
        total_write = Column(Integer)
        total_errors = Column(Integer)

    with Session(mssql_engine) as mssql_db:
        obj = mssql_db.query(ErpItemTransactionBcr).filter(ErpItemTransactionBcr.cpu_busy == 23).first()

        return {"success": obj}
