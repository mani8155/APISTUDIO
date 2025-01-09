from urllib.parse import quote_plus
import requests
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, Date
from sqlalchemy.orm import declarative_base, Session

def custom_api(db, data):
    password_encoded = quote_plus(db["db_password"])
    mysql_connection = f'{db["db_engine"]}+pymysql://{db["db_user"]}:{password_encoded}@{db["db_host"]}:{db["db_port"]}/{db["db_name"]}'
    mysql_engine = create_engine(mysql_connection)
    Base = declarative_base()

    class B2e_Student_Attendance(Base):
        __tablename__ = 'b2e_tbl_col_stuatdhdr'

        attkey = Column(Integer, primary_key=True)
        atdclassid = Column(Integer)
        atdsem = Column(Integer)
        atddate = Column(Date)
        atdperiod = Column(Integer)
        atdstatus = Column(String)
        franchiseid = Column(Integer)
        processid = Column(Integer)
        wfstatus = Column(String)
        revision = Column(Integer)
        createdby = Column(String)
        createdon = Column(DateTime)

    class B2e_Student_Detail(Base):
        __tablename__ = 'b2e_tbl_col_stuatddtl'

        atd_id = Column(Integer, primary_key=True)
        atd_attkey = Column(Integer)
        atd_reason = Column(String)
        atd_status = Column(String)
        atd_subjectkey = Column(Integer)
        atd_staffkey = Column(Integer)
        atd_stdid = Column(Integer)

    with Session(mysql_engine) as mysql_db:
        new_record = B2e_Student_Attendance(
            atdclassid=data.get('atdclassid'),
            atdsem=data.get('atdsem'),
            atddate=data.get('atddate'),
            atdperiod=data.get('atdperiod'),
            atdstatus=data.get('atdstatus'),
            franchiseid=data.get('franchiseid'),
            processid=data.get('processid'),
            wfstatus=data.get('wfstatus'),
            revision=data.get('revision'),
            createdby=data.get('createdby'),
            createdon=data.get('createdon') or datetime.now()
        )

        mysql_db.add(new_record)
        mysql_db.commit()
        mysql_db.refresh(new_record)

        parent_id = new_record.attkey
        print(f"Inserted parent record ID: {parent_id}")

        # Insert child records
        child_data = data.get("child_data", [])
        child_records = []
        for child in child_data:
            child_records.append(B2e_Student_Detail(
                atd_attkey=parent_id,  # Link child to parent
                atd_reason=child.get('atd_reason'),
                atd_status=child.get('atd_status'),
                atd_subjectkey=child.get('atd_subjectkey'),
                atd_staffkey=child.get('atd_staffkey'),
                atd_stdid=child.get('atd_stdid')
            ))

        # Bulk add all child records
        mysql_db.add_all(child_records)
        mysql_db.commit()
        print(f"Inserted {len(child_records)} child records successfully.")

        return {"message": "Data Inserted Successfully"}

# Ensure the correct invocation of the function in your application.
