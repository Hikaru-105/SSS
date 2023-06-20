import sqlite3
DATABASE = 'database.db'

#テーブル削除用

con = sqlite3.connect(DATABASE)
cur = con.cursor()
cur.execute("DELETE FROM schedule")
cur.commit()
con.close()
