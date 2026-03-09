import pandas as pd
from sqlalchemy import create_engine
import pymysql

CSV_FILE_PATH = '/workspaces/data-analysis/data/NBA Team Stats.csv'  # Make sure the file is in the same directory as the script
DB_USER = 'root'
DB_PASSWORD = 'password'
DB_HOST = 'localhost'
DB_NAME = 'data-analysis'
DB_TABLE_NAME = 'nba_team_stats'

try:
    # 1. Read the CSV file into a pandas DataFrame
    df = pd.read_csv(CSV_FILE_PATH)
    print(f"Successfully read {len(df)} rows from {CSV_FILE_PATH}")

    # 2. Create the database connection engine
    # The format is "mysql+pymysql://user:password@host/database"
    connection_string = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    engine = create_engine(connection_string)

    df.to_sql(
        name=DB_TABLE_NAME,
        con=engine,
        if_exists='append',
        index=False # Set to False to prevent pandas from writing the index as a column
    )

    print(f"Successfully imported data into table '{DB_TABLE_NAME}'")

except FileNotFoundError:
    print(f"Error: The file '{CSV_FILE_PATH}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Ensure the connection is closed (SQLAlchemy engine handles connections, but good practice to know)
    if 'engine' in locals() and engine:
        engine.dispose()

