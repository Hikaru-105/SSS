from SSS import app
from flask import render_template
import datetime
import calendar
import sqlite3
DATABASE = 'SSS/db/database.db'


@app.route('/')
def index():
    today = datetime.datetime.now()
    month_first = datetime.datetime(today.year, today.month,1)
    day_upper_left = month_first.weekday() * -1
    month_last_day = calendar.monthrange(today.year, today.month)[1]
    if day_upper_left == -6:
        day_upper_left = 1
    return render_template(
        'I_Schedule/index.html',
        today = today,
        month_last_day = month_last_day,
        day_upper_left = day_upper_left
    )

@app.route('/edit/<int:year>-<int:month>-<int:date>')
def edit(year,month,date):
    user_id = 0
    con = sqlite3.connect(DATABASE)
    #ログインと結合テストするときにセッションから取得
    cur = con.cursor()
    cur.execute("SELECT * FROM schedule WHERE user_id = " + str(user_id) + ORDER BY start_time)
    schedules_this_date = cur.fetchall()
    con.close()
    return render_template(
        'I_Schedule/edit.html',
        year = year,
        month = month,
        date = date,
        schedules_this_date = schedules_this_date
    )
