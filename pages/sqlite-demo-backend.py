"""Demonstrate writing to a SQLite DB while Dash UI is reading from the DB.

Based on: https://medium.com/analytics-vidhya/programming-with-databases-in-python-using-sqlite-4cecbef51ab9

"""

import random
import sqlite3
import time
from pathlib import Path

from tqdm import tqdm

dbFile = Path.cwd() / 'pages/assets/sqlite-demo.sqlite'
dbFile.unlink()  # FIXME: Only for development
conn = sqlite3.connect(dbFile)
cursor = conn.cursor()

cursor.execute("""CREATE TABLE SCHOOL
         (ID INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         AGE            INT     NOT NULL,
         ADDRESS        CHAR(50),
         MARKS          INT);""")
conn.commit()

cursor.execute('INSERT INTO SCHOOL (ID,NAME,AGE,ADDRESS,MARKS)'
               "VALUES (1, 'Rohan', 14, 'Delhi', 200)")
cursor.execute('INSERT INTO SCHOOL (ID,NAME,AGE,ADDRESS,MARKS)'
               "VALUES (2, 'Allen', 14, 'Bangalore', 150 )")
cursor.execute('INSERT INTO SCHOOL (ID,NAME,AGE,ADDRESS,MARKS)'
               "VALUES (3, 'Martha', 15, 'Hyderabad', 200 )")
cursor.execute('INSERT INTO SCHOOL (ID,NAME,AGE,ADDRESS,MARKS)'
               "VALUES (4, 'Palak', 15, 'Kolkata', 650)")
conn.commit()

for _i in tqdm(range(5, 900)):
    cursor.execute(
        'INSERT INTO SCHOOL (ID,NAME,AGE,ADDRESS,MARKS)'
        "VALUES ({}, 'idx-{}', {}, 'COUNTRY', 400)".format(_i, _i, random.randint(1, 40)),
    )
    conn.commit()
    time.sleep(1)


conn.close()
