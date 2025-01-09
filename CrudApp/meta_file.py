# from sqlalchemy import create_engine, MetaData
# from models import TableList as Base1
# from gen_models import Table1 as Base2
# from database import engine

# # Create a new MetaData object and include metadata from both models
# target_metadata = MetaData()
# Base1.metadata.create_all(engine, checkfirst=True)
# Base2.metadata.create_all(engine, checkfirst=True)

# # Add the tables from both models to the target_metadata
# for table in Base1.metadata.tables.values():
#     target_metadata.tables[table.name] = table

# for table in Base2.metadata.tables.values():
#     target_metadata.tables[table.name] = table