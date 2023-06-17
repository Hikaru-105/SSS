import sqlite3
DATABASE = 'database.db'

con = sqlite3.connect(DATABASE)
cur = con.cursor()
cur.execute("SELECT schedule_id FROM schedule")
data = cur.fetchall()
print(data[0])
con.close()
