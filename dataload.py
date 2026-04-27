import oracledb
import csv
import os

# --- SETUP ---
LIB_DIR = "instantclient_23_0"
DB_USER = "PLACEHOLDER"
DB_PASS = "PLACEHOLDER"
DB_DSN = "PLACEHOLDER"

oracledb.init_oracle_client(lib_dir=LIB_DIR)


def load_csv_to_db(cursor, file_name, sql_query):
    file_path = os.path.join('data', file_name)
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found. Skipping...")
        return

    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header
        data = [row for row in reader]
        if data:
            cursor.executemany(sql_query, data)
            print(f"Successfully loaded {len(data)} records from {file_name}")


def run_upload():
    conn = None
    try:
        conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
        cursor = conn.cursor()

        print("Cleaning tables for fresh upload...")
        for table in ["transactions", "credit_cards", "users", "merchants"]:
            cursor.execute(f"DELETE FROM {table}")

        sql_users = "INSERT INTO users VALUES (:1, :2, :3, :4, :5)"
        sql_merch = "INSERT INTO merchants VALUES (:1, :2, :3)"

        sql_cards = "INSERT INTO credit_cards VALUES (:1, :2, TO_DATE(:3, 'YYYY-MM-DD'), :4, :5)"

        sql_trans = f"INSERT INTO transactions VALUES ({','.join([':' + str(i + 1) for i in range(34)])})"

        print("Starting bulk upload from 'data' folder...")
        load_csv_to_db(cursor, 'users.csv', sql_users)
        load_csv_to_db(cursor, 'merchants.csv', sql_merch)
        load_csv_to_db(cursor, 'cards.csv', sql_cards)
        load_csv_to_db(cursor, 'transactions.csv', sql_trans)

        conn.commit()
        print("\nAll CSV data from 'data/' folder has been uploaded!")

    except Exception as e:
        print(f"Error: {e}")
        if conn: conn.rollback()
    finally:
        if conn: conn.close()


if __name__ == "__main__":
    run_upload()
