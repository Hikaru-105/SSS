import sqlite3

def searchGroup(group_name, group_pass):
    group_id = 0
    dbname = "joinGroup.db" # データベースの名前
    con = sqlite3.connect(dbname)

    cur = con.cursor()
    # SELECT グループID FROM テーブル名(グループ情報) WHERE グループ名=group_name AND 合言葉=group_pass
    sql = "SELECT groupid FROM JOINGR WHERE name='" + str(group_name) + "' AND pass='" + str(group_pass) + "'"
    cur.execute(sql)

    res = cur.fetchone()
    if res != None:
        group_id = res[0]

    con.close()
    return int(group_id)