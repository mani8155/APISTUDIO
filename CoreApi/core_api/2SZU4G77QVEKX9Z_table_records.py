# from sqlalchemy import create_engine, text
#
# db_user = 'postgres'
# db_password = 'nanox'
# db_host = 'localhost'
# db_port = '5432'
# db_name = 'nanox'
#
# # Create a connection string
# connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
#
# # Create an SQLAlchemy engine
# engine = create_engine(connection_string)
#
# # Specify the schema name and table name
# schema_name = 'capture'
# table_name = 'pdf_files'
#
# # Create a query to retrieve records from the specified table
# query = text(f"SELECT * FROM {schema_name}.{table_name}")
#
# # Create a connection to the database
# with engine.connect() as connection:
#     # Execute the query
#     result = connection.execute(query)
#
#     # Fetch all records from the result
#     records = result.fetchall()
#
# # Print the records from the "pdf_files" table
# for record in records:
#     print(record)


from sqlalchemy import create_engine, MetaData

# Database connection parameters
db_user = 'postgres'
db_password = 'nanox'
db_host = 'localhost'
db_port = '5432'
db_name = 'nanox'

# Create a connection string
connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(connection_string)

schema_name = 'capture'
table_name = 'pdf_files'

conn = engine.connect()

metadata = MetaData()

metadata.reflect(bind=engine, schema=schema_name, only=[table_name])

pdf_files = metadata.tables[schema_name + '.' + table_name]

query = pdf_files.select()

result = conn.execute(query)

all_values = []

for row in result:
    row_values = list(row)  # Convert the row to a list
    all_values.append(row_values)

conn.close()


print(all_values)