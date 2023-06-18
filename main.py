from SSS import app
from SSS import db
from flask import render_template, redirect, request, url_for
import datetime
import calendar
import sqlite3
import random

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
    user_id = 0#結合テストするときにログイン情報から取得
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * FROM schedule WHERE user_id = " + str(user_id) + " AND year = " +str(year)+ " AND month = " +str(month)+ " AND date = " +str(date)+ " ORDER BY start_time")
    schedules_this_date = cur.fetchall()
    con.close()
    return render_template(
        'I_Schedule/edit.html',
        user_id = user_id,
        year = year,
        month = month,
        date = date,
        schedules_this_date = schedules_this_date
    )

@app.route('/submit_schedule/<int:user_id>-<int:year>-<int:month>-<int:date>', methods=['POST'])
def submit_schedule(user_id, year, month, date):
    sche_name = request.form.getlist('schedule_name')
    start_hour = list(map(int, request.form.getlist('start_hour')))
    start_minute = list(map(int, request.form.getlist('start_minute')))
    end_hour = list(map(int, request.form.getlist('end_hour')))
    end_minute = list(map(int, request.form.getlist('end_minute')))
    years = [year]
    months = [month]
    dates = [date]
    delete_schedules = tuple(map(int, request.form.getlist('delete_this_schedule')))
    edit_schedule(sche_name, user_id, years, months, dates, start_hour, start_minute, end_hour, end_minute, delete_schedules)
    return redirect(url_for('edit', year=year, month=month, date=date))

@app.route('/edit_weekday/<int:year>-<int:month>')
def edit_weekday(year, month):
    user_id = 0#結合テストするときはログイン情報から取得
    return render_template(
    'I_Schedule/weekdayedit.html',
    user_id = user_id,
    year = year,
    month = month,
    )

@app.route('/submit_weekday_schedule/<int:user_id>-<int:year>-<int:month>', methods=['POST'])
def submit_weekday_schedule(user_id, year, month):
    sche_name = request.form.getlist('schedule_name')
    start_hour = list(map(int, request.form.getlist('start_hour')))
    start_minute = list(map(int, request.form.getlist('start_minute')))
    end_hour = list(map(int, request.form.getlist('end_hour')))
    end_minute = list(map(int, request.form.getlist('end_minute')))
    edit_schedule(sche_name, user_id, year, month, date, start_hour, start_minute, end_hour, end_minute, [])
    return redirect(url_for('monthcalendar', year=year, month=month))


def edit_schedule(sche_name, user_id, years, months, dates, start_hour, start_minute, end_hour, end_minute, delete_schedules):
    new_schedules = []
    overlap = True
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT schedule_id FROM schedule ORDER BY schedule_id")
    id_search = cur.fetchall()
    con.close()
    id_search = [x[0] for x in id_search]
    for i in range(len(sche_name)):
        while overlap:
            schedule_id = random.randint(-2147483648, 2147483647)
            overlap = schedule_id in id_search
        id_search.append(schedule_id)
        start_time = start_hour[i]*3600 + start_minute[i]*60
        end_time = end_hour[i]*3600 + end_minute[i]*60
        new_schedules.append((schedule_id, sche_name[i], user_id, years[i], months[i], dates[i], start_time, end_time))
    db.registar_schedule(new_schedules, delete_schedules)
