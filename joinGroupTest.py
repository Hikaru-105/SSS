import sqlite3

dbname = "joinGroup.db"
con = sqlite3.connect(dbname) #接続
# 処理 ######################################################################
# JOINUS(userid INTEGER PRIMARY KEY, groupid INTEGER)
# JOINGR(groupid INTEGER PRIMARY KEY, name STRING, pass STRING)

cur = con.cursor()
sql = "SELECT * FROM JOINUS" # 表示
cur.execute(sql)
print(cur.fetchall())
sql = "SELECT * FROM JOINGR"
cur.execute(sql)
print(cur.fetchall())
#############################################################################
con.close()
