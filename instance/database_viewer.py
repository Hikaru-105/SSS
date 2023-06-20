import sqlite3
DATABASE = 'user.db'

#データベースファイル総閲覧用

con = sqlite3.connect(DATABASE)
cur = con.cursor()
cur.execute("SELECT * FROM User ORDER BY id")
data = cur.fetchall()
for data in data:
    print(data)
con.close()