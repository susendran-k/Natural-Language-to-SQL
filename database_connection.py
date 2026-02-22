from sqlalchemy import create_engine
from llama_index.core import SQLDatabase
import os

db_pass = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")

# Format: postgresql://[user]:[password]@[host]:[port]/[dbname]
connection_string = f"postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}"

engine = create_engine(connection_string)

sql_database = SQLDatabase(engine, include_tables=["aadhar"])

print("Successfully connected!")
print(f"Tables found: {sql_database.get_usable_table_names()}")