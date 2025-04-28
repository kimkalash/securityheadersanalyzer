from sqlalchemy import create_engine, inspect

# Connect to your SQLite database
engine = create_engine('sqlite:///database.db')

# Create an inspector object
inspector = inspect(engine)

# Get a list of all table names
tables = inspector.get_table_names()

# Print the tables
print("Tables in the database:", tables)