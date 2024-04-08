import mysql.connector
import random
from datetime import datetime, timedelta

# Establish a database connection
db = mysql.connector.connect(
    host="mysql",
    user="app",
    passwd="secret",
    database="app",
)

cursor = db.cursor()


# Function to generate a random date
def random_date():
    start_date = datetime(1950, 1, 1)
    end_date = datetime(2000, 12, 31)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    date = start_date + timedelta(days=random_number_of_days)
    return date.strftime('%Y-%m-%d')


# Batch insert size
batch_size = 10000  # Adjust based on your system's capabilities

for _ in range(40000000 // batch_size):
    values = []
    for _ in range(batch_size):
        # Assuming username is "user" + a unique number, and a simple password
        username = f'user{random.randint(1, 100000000)}'
        password = 'password'
        birth_date = random_date()
        values.append((username, password, birth_date))

    query = "INSERT INTO users (username, password, birth_date) VALUES (%s, %s, %s)"
    cursor.executemany(query, values)
    db.commit()

# Close connection
cursor.close()
db.close()
