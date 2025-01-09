from fastapi import FastAPI, HTTPException, Depends
import models
import json
from database import Base

cashed_model = {}


# def get_model(api_name, db):
#     api_details = db.query(models.ApiMeta).filter_by(api_name=api_name).first()
#     if not api_details:
#         raise HTTPException(status_code=404, detail="Api not found")
#     if api_details.api_method != "post":
#         raise HTTPException(status_code=405, detail="Method not allowed")
#     api_data = json.loads(api_details.table_details)
#     if len(api_data) > 1:
#         raise HTTPException(status_code=403, detail="Can not retreive data from 2 tables")
#     table_name = next(iter(api_data))
#     if table_name:
#         try:
#             table = cashed_model[table_name]
#         except KeyError:
#             table_data = db.query(models.Table).filter_by(table_name=table_name).first()
#             if not table_data.published:
#                 raise HTTPException(status_code=403, detail="Table not published")
#             table = models.create_model(table_data)
#             cashed_model[table_name] = table
#         class NewModel(Base):
#             __table__ = table

#         return NewModel
#     raise HTTPException(status_code=403, detail="No Table is found in the api")


def get_model(api_details, db):
    table_details = db.query(models.Table).filter_by(table_name=api_details.api_name).first()
    for field in table_details.fields:
        print(field.field_name)
