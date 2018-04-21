#!/usr/bin/env python
# coding:utf-8

import MySQLdb
import pandas as pd

conn = MySQLdb.connect(host="localhost", user="root", passwd="188113236", db="Plants")
cursor = conn.cursor()

cursor.execute('SELECT * FROM table1');

rows = cursor.fetchall()
length = len(rows)
str(rows)[0:720]
df = pd.DataFrame( [[ij for ij in i] for i in rows] )
df.rename(columns={0: 'id', 1: 'Time', 2: 'temperature', 3: 'soil_humidity', 4: 'humidity', 5: 'light'}, inplace=True);
print df
