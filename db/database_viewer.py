import sqlite3
DATABASE = 'database.db'

#データベースファイル総閲覧用

con = sqlite3.connect(DATABASE)
cur = con.cursor()
cur.execute("SELECT * FROM schedule ORDER BY date")
data = cur.fetchall()
for data in data:
    print(data)
con.close()
