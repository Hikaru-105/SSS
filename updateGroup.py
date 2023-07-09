import sqlite3

###################################################################################################
# Function Name...updateGroup
# Designer........越村太一
# Modifier........渡邉優太
# Function........ユーザID、グループIDを受け取り、更新する
# Return..........なし
###################################################################################################

DATABASE = 'database.db'

def updateGroup(user_id, group_id):
    con = sqlite3.connect(DATABASE)

    cur = con.cursor()
    # UPDATE テーブル名(ユーザ情報) SET グループID=group_id WHERE ユーザID=user_id
    sql = "UPDATE user SET 'group'=" + str(group_id) + " WHERE id=" + str(user_id)
    cur.execute(sql)

    con.commit()
    con.close()
