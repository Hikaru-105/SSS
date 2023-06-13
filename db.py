import sqlite3

DATABASE = 'SSS/db/database.db'

def create_schedule_table():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS schedule (schedule_id, schedule_name, user_id, year, month, date, start_time, end_time)")
    cur.execute("SELECT schedule_id FROM schedule WHERE schedule_name = 'unused' AND year = " +str(year)+ " AND month = " +str(month)+ " AND date = " +str(date))
    data = cur.fetchall()
    if data == []:
        cur.execute("INSERT INTO schedule VALUES(0,'unused',0,2023,6,1,0,7200)")
        cur.execute("INSERT INTO schedule VALUES(1,'unused',0,2023,6,1,54000,81000)")
        cur.execute("INSERT INTO schedule VALUES(2,'unused',0,2023,6,1,18000,39600)")
        cur.execute("INSERT INTO schedule VALUES(3,'unused',0,2023,6,1,14400,16200)")
        cur.execute("INSERT INTO schedule VALUES(4,'unused',1,2023,6,1,0,1800)")
        cur.execute("INSERT INTO schedule VALUES(5,'unused',1,2023,6,1,0,1800)")
        con.commit()
    con.close()

def edit_schedule(user_id, new_schedules, delete_schedules):
    pass
