from urllib.parse import quote_plus

import requests
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base, Session


def custom_api(db, data):
    password_encoded = quote_plus(db["db_password"])
    mysql_connection = f'{db["db_engine"]}+pymysql://{db["db_user"]}:{password_encoded}@{db["db_host"]}:{db["db_port"]}/{db["db_name"]}'
    mysql_engine = create_engine(mysql_connection)
    Base = declarative_base()

    irn_value = data.get('irn')


    class ErpItemTransactionBcr(Base):
      __tablename__ = 'b2e_tbl_erp_itemtransactionsub'
    
      credit_note_no = Column(Integer, primary_key=True)
      irn = Column(String)
      irnstatus = Column(String)

    

  
    
    with Session(mysql_engine) as mysql_db:
      obj = mysql_db.query(ErpItemTransactionBcr).filter(ErpItemTransactionBcr.credit_note_no == credit_note_no).first()
      obj.irn = irn_value
      obj.irnstatus = "IRN_GENERATED"


      mysql_db.add(obj)
      mysql_db.commit()
      mysql_db.refresh(obj)

      return {"message": "IRN successfully generated"}
