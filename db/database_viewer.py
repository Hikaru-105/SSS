import sqlite3
DATABASE = 'database.db'

con = sqlite3.connect(DATABASE)
cur = con.cursor()
cur.execute("SELECT * FROM schedule")
data = cur.fetchall()
print(data)
con.close()
