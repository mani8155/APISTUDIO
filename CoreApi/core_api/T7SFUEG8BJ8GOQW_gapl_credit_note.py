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

  token = data.get('auth_token')

  return token

  # class ErpItemTransactionSub(Base):
  #   __tablename__ = 'b2e_tbl_erp_itemtransactionsub'
  #
  #   itrid = Column(Integer, primary_key=True)
  #   transportdocno = Column(String)
  #   transportdocdate = Column(String)
  #   vehicleno = Column(String)
  #   vehicletype = Column(String)
  #   ewytransportmode = Column(String)
  #   transportid = Column(String)
  #   transportname = Column(String)
  #   transportgst = Column(String)
  #   ewaybillno = Column(String)
  #   ewaybilldate = Column(String)
  #   ewaybillvalidity = Column(String)
  #
  # eway_res = data.get('eway_res')
  # nested_response = eway_res['response']
  #
  # EwbNo = nested_response['EwbNo']
  # EwbDt = nested_response['EwbDt']
  # EwbValidTill = nested_response['EwbValidTill']
  #
  # itrid = data.get('itr_id')
  # transportdocno = data.get('transportdocno')
  # transportdocdate = data.get('transportdocdate')
  # vehicleno = data.get('vehicleno')
  # vehicletype = data.get('vehicletype')
  # ewytransportmode = data.get('ewytransportmode')
  # transportid = data.get('transportid')
  # transportname = data.get('transportname')
  # transportgst = data.get('transportgst')
  #
  # with Session(mysql_engine) as mysql_db:
  #   obj = mysql_db.query(ErpItemTransactionSub).filter(ErpItemTransactionSub.itrid == itrid).first()
  #   obj.transportdocno = transportdocno
  #   obj.transportdocdate = transportdocdate
  #   obj.vehicleno = vehicleno
  #   obj.vehicletype = vehicletype
  #   obj.ewytransportmode = ewytransportmode
  #   obj.transportdocdate = transportdocdate
  #   obj.transportid = transportid
  #   obj.transportname = transportname
  #   obj.transportgst = transportgst
  #   obj.ewaybillno = EwbNo
  #   obj.ewaybilldate = EwbDt
  #   obj.ewaybillvalidity = EwbValidTill
  #   mysql_db.add(obj)
  #   mysql_db.commit()
  #   mysql_db.refresh(obj)

    # return {"message": "e-WayBill successfully generated"}
