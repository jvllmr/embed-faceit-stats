import sqlite3, os

if not "database.db" in os.listdir():
    sql = sqlite3.connect("database.db")
    sql.execute("create table lastrefresh (name text, date text)")
    sql.commit()
else:
    sql = sqlite3.connect("database.db")