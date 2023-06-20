import sqlite3

def updateGroup(user_id, group_id):
    dbname = "joinGroup.db" # データベースの名前
    con = sqlite3.connect(dbname)

    cur = con.cursor()
    # UPDATE テーブル名(ユーザ情報) SET グループID=group_id WHERE ユーザID=user_id
    sql = "UPDATE JOINUS SET groupid=" + str(group_id) + " WHERE userid=" + str(user_id)
    cur.execute(sql)

    con.commit()
    con.close()