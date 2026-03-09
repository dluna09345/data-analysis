from sqlalchemy import create_engine, inspect, text

def check_nulls_and_duplicates(database_url):

    table_name = "nba_team_stats"

    engine = create_engine(database_url)
    inspector = inspect(engine)

    columns = [col["name"] for col in inspector.get_columns(table_name)]

    print(f"\nChecking table: {table_name}")
    print("=" * 60)

    with engine.connect() as conn:

        total_rows = conn.execute(
            text(f"SELECT COUNT(*) FROM `{table_name}`")
        ).scalar()

        print(f"Total rows before cleaning: {total_rows}\n")

        if total_rows == 0:
            print("Table is empty!")
            return

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


        print("\nChecking for exact duplicate rows...")

        conn.execute(text(f"""
            CREATE TABLE nba_team_stats_clean AS
            SELECT DISTINCT *
            FROM `{table_name}`
        """))

        cleaned_rows = conn.execute(
            text("SELECT COUNT(*) FROM nba_team_stats_clean")
        ).scalar()

        duplicates_removed = total_rows - cleaned_rows

        if duplicates_removed > 0:
            print(f"⚠ Removed {duplicates_removed} duplicate rows.")

            conn.execute(text(f"DROP TABLE `{table_name}`"))
            conn.execute(text("RENAME TABLE nba_team_stats_clean TO nba_team_stats"))

            print("✓ Table cleaned successfully.")
        else:
            conn.execute(text("DROP TABLE nba_team_stats_clean"))
            print("✓ No duplicate rows found.")

        final_rows = conn.execute(
            text(f"SELECT COUNT(*) FROM `{table_name}`")
        ).scalar()

        print(f"\nFinal row count: {final_rows}")




if __name__ == "__main__":

    DB_USER = "root"
    DB_PASSWORD = "password"
    DB_HOST = "localhost"
    DB_NAME = "data-analysis"

    database_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

    check_nulls_and_duplicates(database_url)