import sqlite3
DATABASE = 'user.db'

#データベースファイル総閲覧用

con = sqlite3.connect(DATABASE)
cur = con.cursor()
cur.execute("SELECT * FROM user")
datas = cur.fetchall()
for data in datas:
    print(data)
con.close()
