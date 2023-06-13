from SSS import app
from flask import render_template
import datetime
import calendar
import sqlite3
DATABASE = 'SSS/db/database.db'


@app.route('/monthcalendar/<int:year>-<int:month>')
def monthcalendar(year, month):#結合テストではログイン後に取得したtoday = datetime.datetime.now()からyearとmonthを持ってくる。
    today = datetime.datetime.now()
    month_first = datetime.datetime(year, month,1)
    day_upper_left = month_first.weekday() * -1
    month_last_day = calendar.monthrange(year, month)[1]
    if day_upper_left == -6:
        day_upper_left = 1
    return render_template(
        'I_Schedule/monthcalendar.html',
        year = year,
        month = month,
        month_last_day = month_last_day,
        day_upper_left = day_upper_left
    )

@app.route('/edit/<int:year>-<int:month>-<int:date>')
def edit(year,month,date):
    user_id = 0#ログインと結合テストするときにセッションから取得
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * FROM schedule WHERE user_id = " + str(user_id) + " AND year = " +str(year)+ " AND month = " +str(month)+ " AND date = " +str(date)+ " ORDER BY start_time")
    schedules_this_date = cur.fetchall()
    con.close()
    return render_template(
        'I_Schedule/edit.html',
        year = year,
        month = month,
        date = date,
        schedules_this_date = schedules_this_date
    )

@app.route('/send_schedule/<int:year>-<int:month>-<int:date>', methods=['POST'])
def send_schedule():
    pass
