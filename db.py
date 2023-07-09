import sqlite3

MYDATABASE = 'database.db'

def create_schedule_table():
    #データベース接続
    con = sqlite3.connect(MYDATABASE)
    cur = con.cursor()
    con.execute("CREATE TABLE IF NOT EXISTS schedule (schedule_id INTEGER, schedule_name TEXT, user_id INTEGER, year INTEGER, month INTEGER, date INTEGER, start_time INTEGER, end_time TNTEGER)")
    con.execute("CREATE TABLE IF NOT EXISTS kokyaku (user_id INTEGER, username TEXT, password TEXT, gpid INTEGER)")
    con.execute("CREATE TABLE IF NOT EXISTS kyaku (user_id INTEGER, username TEXT, password TEXT, gpid INTEGER)")
    cur.execute("SELECT schedule_id FROM schedule WHERE schedule_name = 'unused'")
    data = cur.fetchall()
    #データベースが空ならば仮データ登録
    
    cur.execute("INSERT INTO schedule VALUES(0,'unused',0,2023,6,1,0,1800)")#0~2
    cur.execute("INSERT INTO schedule VALUES(1,'unused',0,2023,6,2,54000,81000)")#15~22.5
    cur.execute("INSERT INTO schedule VALUES(2,'unused',0,2023,6,2,18000,39600)")#5~11
    cur.execute("INSERT INTO schedule VALUES(3,'unused',0,2023,6,2,14400,16200)")#4~4.5
    cur.execute("INSERT INTO schedule VALUES(3,'unused',0,2023,5,2,0,86400)")#4~4.5
    cur.execute("INSERT INTO schedule VALUES(4,'unused',1,2023,6,2,0,81000)")#0~0.5
    cur.execute("INSERT INTO schedule VALUES(5,'unused',2,2023,6,2,0,1800)")
    cur.execute("INSERT INTO schedule VALUES(7,'unused',2,2023,6,2,84600,86400)")
    cur.execute("INSERT INTO schedule VALUES(8,'unused',2,2023,6,2,1800,84600)")
    cur.execute("INSERT INTO schedule VALUES(9,'unused',0,2023,11,7,0,1800)")
    cur.execute("INSERT INTO schedule VALUES(10,'unused',1,2023,11,8,1800,68400)")
    cur.execute("INSERT INTO schedule VALUES(6,'unused',2,2023,11,9,68400,86400)")
    cur.execute("INSERT INTO schedule VALUES(6,'unused',2,2023,11,11,0,84600)")

    cur.execute("INSERT INTO kyaku VALUES(0,'hikaru','2000',1005)")
    cur.execute("INSERT INTO kyaku VALUES(1,'yokunan','2000',10030)")
    cur.execute("INSERT INTO kyaku VALUES(2,'kamui','634',1005)")
    con.commit()
    con.close()

