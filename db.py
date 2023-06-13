import sqlite3

DATABASE = 'SSS/db/database.db'

def create_schedule_table():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS schedule (schedule_id, schedule_name, user_id, year, month, day, start_time, end_time)")
    cur.execute("SELECT schedule_id FROM schedule WHERE schedule_name = 'unused'")
    data = cur.fetchall()
    if data == []:
        cur.execute("INSERT INTO schedule VALUES(0,'unused',0,0,0,0,0,43200)")
        cur.execute("INSERT INTO schedule VALUES(1,'unused',0,1,1,1,43200,86400)")
        cur.execute("INSERT INTO schedule VALUES(2,'unused',1,2,2,2,2,2)")
        cur.execute("INSERT INTO schedule VALUES(3,'unused',1,3,3,3,3,3)")
    con.commit()
    con.close()
