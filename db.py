import sqlite3

DATABASE = 'SSS/instance/database.db'

def create_schedule_table():
    #データベース接続
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    #テーブルが無ければ作成
    cur.execute("CREATE TABLE IF NOT EXISTS schedule (schedule_id, schedule_name, user_id, year, month, date, start_time, end_time)")
    cur.execute("SELECT schedule_id FROM schedule WHERE schedule_name = 'unused'")
    data = cur.fetchall()
    #データベースが空ならば仮データ登録
    if not data:
        cur.execute("INSERT INTO schedule VALUES(0,'unused',0,2023,6,1,0,7200)")
        cur.execute("INSERT INTO schedule VALUES(1,'unused',0,2023,6,1,54000,81000)")
        cur.execute("INSERT INTO schedule VALUES(2,'unused',0,2023,6,1,18000,39600)")
        cur.execute("INSERT INTO schedule VALUES(3,'unused',0,2023,6,1,14400,16200)")
        cur.execute("INSERT INTO schedule VALUES(4,'unused',1,2023,6,1,0,1800)")
        cur.execute("INSERT INTO schedule VALUES(5,'unused',1,2023,6,1,0,1800)")
        con.commit()
    con.close()

#データベースへスケジュール情報を登録
def registar_schedule(new_schedules, delete_schedules):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    sql = "INSERT INTO schedule VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
    for new_schedule in new_schedules:
        if new_schedule[6] == 0 and new_schedule[7] == 0:
            continue
        cur.execute(sql,new_schedule)
    #削除するスケジュールがあればデータベースから削除
    if delete_schedules:
        sql = "DELETE FROM schedule WHERE schedule_id IN ({})".format(','.join(['?'] * len(delete_schedules)))
        cur.execute(sql,delete_schedules)
    con.commit()
    con.close()
