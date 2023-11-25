import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE mq135-data ( TEXT, addr TEXT,  pin TEXT)')
print("Table created successfully")

conn.execute('CREATE TABLE pm25-data (name TEXT, addr TEXT, pin TEXT)')
print("Table created successfully")

conn.close()