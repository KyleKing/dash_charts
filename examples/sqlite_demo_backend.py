"""Demonstrate writing to a SQLite DB while Dash UI is reading from the DB.

Based on: https://medium.com/analytics-vidhya/programming-with-databases-in-python-using-sqlite-4cecbef51ab9

"""

import sqlite3
import time
from pathlib import Path

import numpy as np
from tqdm import tqdm

dbFile = Path.cwd() / 'examples/assets/sqlite-demo.sqlite'
points = 1000
delay = 0.1  # time between new data points in seconds

if __name__ == '__main__':
    dbFile.unlink()  # Reset database on each iteration
    conn = sqlite3.connect(dbFile)
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE EVENTS (
        ID   INT   PRIMARY KEY   NOT NULL,
        LABEL   TEXT   NOT NULL,
        VALUE   INT   NOT NULL
    );""")
    conn.commit()

    # Generate random data points
    mu, sigma = (10, 8)  # mean and standard deviation
    samples = np.random.normal(mu, sigma, points)

    # Fill the database with sample data
    for _i in tqdm(range(points)):
        val = (-1 if _i > 500 else 1) * _i / 10.0  # Make the graph kind of interesting
        cursor.execute('INSERT INTO EVENTS (ID,LABEL,VALUE) VALUES ({}, "idx-{}", {})'.format(_i, _i, samples[_i] + val))
        conn.commit()
        time.sleep(delay)

    conn.close()
