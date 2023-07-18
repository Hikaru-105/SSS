import sqlite3

###################################################################################################
# Function Name...searchGroup
# Designer........越村太一
# Function........グループIDを受け取り、そのグループIDが存在するか返す
# Return..........グループIDが見つかる         : True
#                 else                       : False
###################################################################################################

DATABASE = 'instance/database.db'

def searchGroup(group_id, keyword):
    # 登録済みのGroupIDリストを作成
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT group_id FROM 'group' ORDER BY group_id")
    id_search = cur.fetchall()
    id_search = [x[0] for x in id_search]
    existence = group_id in id_search
    if not existence:
        con.close()
        return existence
    cur.execute("SELECT keyword FROM 'group' WHERE group_id="+str(group_id))
    keyword_db = cur.fetchone()[0]
    con.close()
    existence = keyword == keyword_db
    return existence
