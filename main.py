from sqlalchemy import create_engine
from llama_index.core import SQLDatabase

# Format: postgresql://[user]:[password]@[host]:[port]/[dbname]
connection_string = "postgresql://postgres:your-password@localhost:5432/aadhar_data"

engine = create_engine(connection_string)

sql_database = SQLDatabase(engine, include_tables=["aadhar"])

print("Successfully connected!")
print(f"Tables found: {sql_database.get_usable_table_names()}")