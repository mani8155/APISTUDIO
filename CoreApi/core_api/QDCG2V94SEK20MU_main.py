from sqlalchemy import create_engine, inspect

# database connection parameters
db_user = 'root'
db_password = '25f9e794323b453885f5181f1b624d0b'
# db_password = '123456789'
db_host = 'localhost'
db_port = '3306'
db_name = 'sakila'
db_engine = 'mysql'

db_password_encoded = quote_plus(db_password)

connection_string = f"{db_engine}+mysqlconnector://{db_user}:{db_password_encoded}@{db_host}/{db_name}"

engine = create_engine(connection_string)

metadata = MetaData()

metadata.reflect(bind=engine)

# print("Tables in the database:")
table_list = []
for table in metadata.tables.values():
    table_list.append(table.name)


print(table_list)
