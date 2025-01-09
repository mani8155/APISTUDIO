from urllib.parse import quote_plus
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, Session


def custom_api(db, data):
    # Encoding password and setting up the MySQL connection string
    password_encoded = quote_plus(db["db_password"])
    mysql_connection = f'{db["db_engine"]}+pymysql://{db["db_user"]}:{password_encoded}@{db["db_host"]}:{db["db_port"]}/{db["db_name"]}'
    mysql_engine = create_engine(mysql_connection)
    Base = declarative_base()

    # Extracting data from the request
    atd_attkey = data.get('atd_attkey')
    atd_reason = data.get('atd_reason')
    atd_status = data.get('atd_status')
    atd_subjectkey = data.get('atd_subjectkey')
    atd_staffkey = data.get('atd_staffkey')
    atd_stdid = data.get('atd_stdid')

    # Header-related data
    atd_sem = data.get('atdsem')
    atd_date = data.get('atddate')
    atd_period = data.get('atdperiod')
    atd_status_header = data.get('atdstatus')
    franchise_id = data.get('franchiseid')
    process_id = data.get('processid')
    wf_status = data.get('wfstatus')
    revision = data.get('revision')
    created_by = data.get('createdby')
    created_on = data.get('createdon')

    # Define the header table class
    class B2e_Student_Attendance(Base):
        __tablename__ = 'b2e_tbl_col_stuatdhdr'

        Class_id = Column(Integer, primary_key=True)  # Assuming Class_id is auto-increment
        Atd_attkey = Column(Integer, unique=True)  # Use the atd_attkey as unique identifier
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

    # Define the detail table class
    class B2e_Student_Detail(Base):
        __tablename__ = 'b2e_tbl_col_stuatddtl'

        Atd_attkey = Column(Integer, primary_key=True)
        Atd_reason = Column(String)
        Atd_status = Column(String)
        Atd_subjectkey = Column(Integer)
        Atd_staffkey = Column(Integer)
        Atd_stdid = Column(Integer)
        Atd_classid = Column(Integer)  # Foreign key to Class_id in the header table

    # Start a session to interact with the database
    with Session(mysql_engine) as mysql_db:
        # Insert into the header table if the atd_attkey does not exist
        header_obj = mysql_db.query(B2e_Student_Attendance).filter(
            B2e_Student_Attendance.Atd_attkey == atd_attkey).first()

        if not header_obj:
            # Insert a new record into the header table if it does not exist
            header_obj = B2e_Student_Attendance(
                Atd_attkey=atd_attkey,  # atd_attkey is provided in the input
                Atd_sem=atd_sem,
                Atd_date=atd_date,
                Atd_period=atd_period,
                Atd_status=atd_status_header,
                Franchise_id=franchise_id,
                Process_id=process_id,
                Wf_status=wf_status,
                Revision=revision,
                CreatedBy=created_by,
                CreatedOn=created_on
            )
            mysql_db.add(header_obj)
            mysql_db.commit()  # Commit the insert for the header table
            mysql_db.refresh(header_obj)

        # Now insert into the detail table based on atd_attkey
        detail_obj = mysql_db.query(B2e_Student_Detail).filter(B2e_Student_Detail.Atd_attkey == atd_attkey).first()

        if not detail_obj:
            # Insert a new record into the detail table if it does not exist
            detail_obj = B2e_Student_Detail(
                Atd_attkey=atd_attkey,  # This links the detail record to the header using atd_attkey
                Atd_reason=atd_reason,
                Atd_status=atd_status,
                Atd_subjectkey=atd_subjectkey,
                Atd_staffkey=atd_staffkey,
                Atd_stdid=atd_stdid,
                Atd_classid=header_obj.Class_id  # Use the Class_id from the header record
            )
            mysql_db.add(detail_obj)
            mysql_db.commit()  # Commit the insert for the detail table
            mysql_db.refresh(detail_obj)

            return {"message": "Data Inserted Successfully"}
        else:
            return {"message": "Failed To Insert Data, Detail Already Exists"}