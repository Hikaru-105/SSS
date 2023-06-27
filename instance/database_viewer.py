import sqlite3
<<<<<<< HEAD
DATABASE = 'database.db'
=======
DATABASE = 'user.db'
>>>>>>> da2144a8877be094923fca9911f66a62437838c8

#データベースファイル総閲覧用

con = sqlite3.connect(DATABASE)
cur = con.cursor()
<<<<<<< HEAD
cur.execute("SELECT * FROM schedule ORDER BY date")
data = cur.fetchall()
for data in data:
    print(data)
con.close()
=======
cur.execute("SELECT * FROM User ORDER BY id")
data = cur.fetchall()
for data in data:
    print(data)
con.close()
>>>>>>> da2144a8877be094923fca9911f66a62437838c8
