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

    class_id = data.get('atdclassid')
    atd_sem = data.get('atdsem')
    atd_date = data.get('atddate')
    atd_period = data.get('atdperiod')
    atd_status = data.get('atdstatus')
    franchise_id = data.get('franchiseid')
    process_id = data.get('processid')
    wf_status = data.get('wfstatus')
    revision = data.get('revision')
    created_by = data.get('createdby')
    created_on = data.get('createdon')
    atd_attkey = data.get('atd_attkey')
    atd_reason = data.get('atd_reason')
    atdd_status = data.get('atd_status')
    atd_subjectkey = data.get('atd_subjectkey')
    atd_staffkey = data.get('atd_staffkey')
    atd_stdid = data.get('atd_stdid')

    class B2e_Student_Attendance(Base):
        __tablename__ = 'b2e_tbl_col_stuatdhdr'

        Class_id = Column(Integer, primary_key=True)
        Atd_sem = Column(Integer)
        Atd_date = Column(DateTime)
        Atd_period = Column(Integer)
        Atd_status = Column(String)
        Franchise_id = Column(Integer)
        Process_id = Column(Integer)
        Wf_status = Column(String)
        Revision = Column(Integer)
        CreatedBy = Column(String)
        CreatedOn = Column(DateTime)

    class B2e_Student_Detail(Base):
        __tablename__ = 'b2e_tbl_col_stuatddtl'

        Atd_attkey = Column(Integer, primary_key=True)
        Atd_reason = Column(String)
        Atd_status = Column(String)
        Atd_subjectkey = Column(Integer)
        Atd_staffkey = Column(Integer)
        Atd_stdid = Column(Integer)

    with Session(mysql_engine) as mysql_db:
        attendance_obj = mysql_db.query(B2e_Student_Attendance).filter(
            B2e_Student_Attendance.Class_id == class_id
        ).first()

        if attendance_obj:
            attendance_obj.Atd_sem = atd_sem
            attendance_obj.Atd_date = atd_date
            attendance_obj.Atd_period = atd_period
            attendance_obj.Atd_status = atd_status
            attendance_obj.Franchise_id = franchise_id
            attendance_obj.Process_id = process_id
            attendance_obj.Wf_status = wf_status
            attendance_obj.Revision = revision
            attendance_obj.CreatedBy = created_by
            attendance_obj.CreatedOn = created_on

            mysql_db.add(attendance_obj)
            mysql_db.commit()
            mysql_db.refresh(attendance_obj)
            return {"message": "Data Inserted Successfully"}

    with Session(mysql_engine) as mysql_db_connection:
        detail_obj = mysql_db_connection.query(B2e_Student_Detail).filter(
            B2e_Student_Detail.Atd_attkey == atd_attkey
        ).first()

        if detail_obj:
            detail_obj.Atd_reason = atd_reason
            detail_obj.Atd_status = atdd_status
            detail_obj.Atd_subjectkey = atd_subjectkey
            detail_obj.Atd_staffkey = atd_staffkey
            detail_obj.Atd_stdid = atd_stdid

            mysql_db_connection.add(detail_obj)
            mysql_db_connection.commit()
            mysql_db_connection.refresh(detail_obj)

            return {"message": "Data Inserted Successfully"}
        else:
            return {"message": "Failed To Insert Data"}
