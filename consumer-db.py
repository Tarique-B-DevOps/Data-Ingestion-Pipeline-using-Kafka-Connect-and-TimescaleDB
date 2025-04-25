import os
import psycopg2
import time

# This script consumes messages from TimescaleDB table.

DB_NAME = os.getenv("PGDATABASE", "timeseries")
DB_USER = os.getenv("PGUSER", "postgres")
DB_PASSWORD = os.getenv("PGPASSWORD", "postgres")
DB_HOST = os.getenv("PGHOST", "localhost")
DB_PORT = os.getenv("PGPORT", "5432")

TABLE_NAME = os.getenv("TABLE_NAME", "sensor_data")

# Track last timestamp seen
last_seen = None

def fetch_new_data(conn):
    global last_seen
    cursor = conn.cursor()

    if last_seen:
        query = f"""
            SELECT * FROM {TABLE_NAME}
            WHERE timestamp > %s
            ORDER BY timestamp ASC
        """
        cursor.execute(query, (last_seen,))
    else:
        query = f"""
            SELECT * FROM {TABLE_NAME}
            ORDER BY timestamp DESC
            LIMIT 5
        """
        cursor.execute(query)

    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(row)
        last_seen = rows[-1][-1]

if __name__ == "__main__":
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    print(f"Connected to TimescaleDB. Listening for new data in '{TABLE_NAME}'...")
    try:
        while True:
            fetch_new_data(conn)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped.")
    finally:
        conn.close()
