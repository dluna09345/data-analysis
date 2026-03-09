from sqlalchemy import create_engine, inspect, text

def check_nulls_and_duplicates(database_url):
    table_name = 'nba_team_stats'  # Set the table name here
    
    # Create engine and connect
    engine = create_engine(database_url)
    inspector = inspect(engine)
    
    # Get column names
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    
    print(f"\nChecking table: {table_name}")
    print("=" * 60)
    
    # Get total row count
    with engine.connect() as conn:
        total_rows = conn.execute(text(f"SELECT COUNT(*) FROM `{table_name}`")).scalar()
        print(f"Total rows: {total_rows}\n")
        
        if total_rows == 0:
            print("Table is empty!")
            return
        
        # Check each column for NULLs
        print(f"{'Column':<30} {'NULLs':<10} {'Percentage'}")
        print("-" * 60)
        
        null_found = False
        for col in columns:
            null_count = conn.execute(
                text(f"SELECT COUNT(*) FROM `{table_name}` WHERE `{col}` IS NULL")
            ).scalar()
            
            if null_count > 0:
                null_found = True
                percentage = (null_count / total_rows) * 100
                print(f"{col:<30} {null_count:<10} {percentage:>6.2f}%")
        
        if not null_found:
            print("✓ No NULL values found!")
        
        # Now check for duplicates
        group_by_cols = ", ".join([f"`{col}`" for col in columns])
        sql = f"""
            SELECT {group_by_cols}, COUNT(*) as count
            FROM `{table_name}`
            GROUP BY {group_by_cols}
            HAVING count > 1
        """
        duplicates = conn.execute(text(sql)).fetchall()
        
        if duplicates:
            print("\nDuplicates found:")
            for row in duplicates:
                print(row)
        else:
            print("\n✓ No duplicates found!")


# Example usage
if __name__ == "__main__":
    # Configure your database connection
    DB_USER = "root"
    DB_PASSWORD = "password"
    DB_HOST = "localhost"
    DB_NAME = "data-analysis"

database_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"           
check_nulls_and_duplicates(database_url)