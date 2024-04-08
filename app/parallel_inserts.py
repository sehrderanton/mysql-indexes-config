import mysql.connector
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
from datetime import datetime, timedelta
import time

# Function to generate a random date
def random_date():
    start_date = datetime(1950, 1, 1)
    end_date = datetime(2000, 12, 31)
    days_between_dates = (end_date - start_date).days
    random_number_of_days = random.randrange(days_between_dates)
    return (start_date + timedelta(days=random_number_of_days)).strftime('%Y-%m-%d')

# Function to perform a single insert
def insert_record(record_id):
    try:
        conn = mysql.connector.connect(
            host="mysql",
            user="app",
            passwd="secret",
            database="app",
        )
        cursor = conn.cursor()
        username = f'user{record_id}'
        password = 'password'
        birth_date = random_date()
        cursor.execute("INSERT INTO users (username, password, birth_date) VALUES (%s, %s, %s)", (username, password, birth_date))
        conn.commit()
        cursor.close()
        conn.close()
        return f'Record {record_id} inserted.'
    except Exception as e:
        return f'Error inserting record {record_id}: {e}'

# Main function to insert records with concurrency
def main():
    start_time = time.time()  # Record the start time

    records_to_insert = 2000
    concurrency_level = 50

    with ThreadPoolExecutor(max_workers=concurrency_level) as executor:
        futures = [executor.submit(insert_record, i) for i in range(records_to_insert)]
        for future in as_completed(futures):
            print(future.result())

    end_time = time.time()  # Record the end time
    print(f"Execution time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
