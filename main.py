from SSS import app
from SSS import db
from flask import render_template, redirect, request, url_for
import datetime
import calendar
import sqlite3
import random

#データベースファイルの位置
DATABASE = 'SSS/instance/database.db'

#ルーティング
@app.route('/monthcalendar/<int:year>-<int:month>')
#カレンダー表示
def monthcalendar(year, month):
    #結合テストではログイン後に取得したtoday = datetime.datetime.now()からyearとmonthを持ってくる。
    #月初めの曜日の算出[0:"月",1:"火",2:"水",3:"木",4:"金",5:"土",6:"日"]
    month_first_day = datetime.datetime(year, month,1)
    #負の数も考慮したカレンダーの一番左上に来る数字を計算
    day_upper_left = month_first_day.weekday() * -1
    if day_upper_left == -6:
        day_upper_left = 1
    #月の最終日を計算
    month_last_day = calendar.monthrange(year, month)[1]

    #返り値を渡すhtmlファイルと引数を指定
    return render_template(
        'I_Schedule/monthcalendar.html',
        year = year,
        month = month,
        month_last_day = month_last_day,
        day_upper_left = day_upper_left
    )

#スケジュール編集する日付を選択
@app.route('/edit/<int:year>-<int:month>-<int:date>')
def edit(year,month,date):
    #結合テストするときにログイン情報から取得
    user_id = 0
    #データベース接続
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    #クエリ実行
    cur.execute("SELECT * FROM schedule WHERE user_id = " +str(user_id)+ " AND year = " +str(year)+ " AND month = " +str(month)+ " AND date = " +str(date)+ " ORDER BY start_time, end_time")
    #クエリ結果取得
    schedules_this_date = cur.fetchall()
    #接続断
    con.close()
    return render_template(
        'I_Schedule/edit.html',
        user_id = user_id,
        year = year,
        month = month,
        date = date,
        schedules_this_date = schedules_this_date
    )

#入力データ処理
@app.route('/submit_schedule/<int:user_id>-<int:year>-<int:month>-<int:date>', methods=['POST'])
def submit_schedule(user_id, year, month, date):
    #入力データをリストに変換
    sche_name = request.form.getlist('schedule_name')
    start_hour = list(map(int, request.form.getlist('start_hour')))
    start_minute = list(map(int, request.form.getlist('start_minute')))
    end_hour = list(map(int, request.form.getlist('end_hour')))
    end_minute = list(map(int, request.form.getlist('end_minute')))
    years = [year]
    months = [month]
    dates = [date]
    #削除するリストは変換処理が無いためデータベースに送るためのタプルに変換
    delete_schedules = tuple(map(int, request.form.getlist('delete_this_schedule')))
    #スケジュールデータ変換処理に入力データを送る
    edit_schedule(sche_name, user_id, years, months, dates, start_hour, start_minute, end_hour, end_minute, delete_schedules)
    #自身へリダイレクトしてページ更新
    return redirect(url_for('edit', year=year, month=month, date=date))

@app.route('/edit_weekday/<int:year>-<int:month>')
def edit_weekday(year, month):
    #結合テストするときはログイン情報から取得
    user_id = 0
    return render_template(
    'I_Schedule/weekdayedit.html',
    user_id = user_id,
    year = year,
    month = month,
    )

@app.route('/submit_weekday_schedule/<int:user_id>-<int:year>-<int:month>', methods=['POST'])
#入力データ処理（曜日スケジュール用）
def submit_weekday_schedule(user_id, year, month):
    sche_name_temp = request.form.getlist('schedule_name')
    start_hour_temp = list(map(int, request.form.getlist('start_hour')))
    start_minute_temp = list(map(int, request.form.getlist('start_minute')))
    end_hour_temp = list(map(int, request.form.getlist('end_hour')))
    end_minute_temp = list(map(int, request.form.getlist('end_minute')))

    #スケジュールデータ変換処理に送るリストの空リストを作成
    years = []
    months = []
    dates = []
    sche_name = []
    start_hour = []
    start_minute = []
    end_hour = []
    end_minute = []

    date_temp = 0

    #月初め、月終わり、カレンダー左上の日付を計算
    month_first_day = datetime.datetime(year, month,1)
    month_last_day = calendar.monthrange(year, month)[1]
    day_upper_left = month_first_day.weekday() * -1
    if day_upper_left == -6:
        day_upper_left = 1

    #曜日ごとにスケジュール情報をリストに追加
    for weekday in range(7):
        date_temp = day_upper_left + weekday
        #date_tempが0以下あるいはmonth_last_dayよりも大きければリストへスケジュール情報を追加しない
        while date_temp < month_last_day:
            if date_temp < 1:
                date_temp += 7
                continue
            years.append(year)
            months.append(month)
            dates.append(date_temp)
            sche_name.append(sche_name_temp[weekday])
            start_hour.append(start_hour_temp[weekday])
            start_minute.append(start_minute_temp[weekday])
            end_hour.append(end_hour_temp[weekday])
            end_minute.append(end_minute_temp[weekday])
            date_temp += 7
    #変換処理にスケジュール情報を渡す
    edit_schedule(sche_name, user_id, years, months, dates, start_hour, start_minute, end_hour, end_minute, [])
    #カレンダー画面（W2個人スケジュール画面）に移動
    return redirect(url_for('monthcalendar', year=year, month=month))


def edit_schedule(sche_name, user_id, years, months, dates, start_hour, start_minute, end_hour, end_minute, delete_schedules):
    #登録処理へ渡すリストの空リストを作成
    new_schedules = []

    #データベースから既存のスケジュールIDを全て取得
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT schedule_id FROM schedule ORDER BY schedule_id")
    id_search = cur.fetchall()
    con.close()
    id_search = [x[0] for x in id_search]
    #スケジュールIDが既存のものと重複しないように生成し、スケジュールのタプルをリストに追加
    for i in range(len(sche_name)):
        overlap = True
        while overlap:
            schedule_id = random.randint(-2147483648, 2147483647)
            overlap = schedule_id in id_search
        id_search.append(schedule_id)
        start_time = start_hour[i]*3600 + start_minute[i]*60
        end_time = end_hour[i]*3600 + end_minute[i]*60
        new_schedules.append((schedule_id, sche_name[i], user_id, years[i], months[i], dates[i], start_time, end_time))
    #登録処理へリストを渡す
    db.registar_schedule(new_schedules, delete_schedules)
