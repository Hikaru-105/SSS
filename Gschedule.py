from SSS import app
from flask import render_template
import datetime
import calendar
import sqlite3
MYDATABASE='database.db'

#データベースファイルの位置

#後で消す
@app.route("/")
def a():
    return render_template('G_Schedule/a.html')

#ルーティング
@app.route("/GSchedule/<int:year>-<int:month>")
#########################################################
###Functionname :Gcalendar()
###Designer     :村田晃琉
###Function     :カレンダーを表示するための
#                   年、月、月初めの曜日、月の最後の日にち
###Return       :
#########################################################
def Gcalendar(year,month,user_id=0):

    year=year
    month=month
    month_first_day=datetime.datetime(year,month,1)
    day_upper_left=month_first_day.weekday()*-1
    if day_upper_left == -6:
        day_upper_left=1
    month_last_day=calendar.monthrange(year,month)[1]

    con=sqlite3.connect(MYDATABASE)
    cur=con.cursor()
    #user_id(最初から保持)でDBから条件を絞りgpidを取得
    db_kyaku=cur.execute('SELECT * FROM kyaku WHERE user_id= '+ str(user_id)).fetchall()
    gpid=db_kyaku[0][3]
    #gpidでDBから条件を絞りグループ全員のuser_idを配列kへ取得
    k=cur.execute('SELECT * FROM kyaku WHERE gpid='+ str(gpid)).fetchall()
    db_schedule=[]
    #year,month,kよりDBからすべてのメンバーのある月のスケジュールを配列db_scheduleへ取得
    for i in k:
        K=i[0]
        db_schedule.append(cur.execute('SELECT * FROM schedule WHERE year= '+ str(year) 
                                       +" AND month= "+ str(month) 
                                       +" AND user_id="+ str(K)).fetchall())
    con.close()

    #どの日付に予定が入っているかの判定
    #すべての日付(配列cl)に予定が入っていない状態(0)とする。
    cl=[0]*32
    RT=[[]for _ in range(32)]

    for i in range(32):
        #mへ30分ごとの一日のスケジュールのlistを格納
        #list(o)の中身は
        # 0b010000000000000000000000000000000000000000111100
        # のように0(予定がない)と1(予定がある)が格納されている。
        #上の例は00:30~01:00と21:00~23:00に予定があることを表す
        o=list(format(Ctimeline(db_schedule, i), '#050b'))
        #zはlistのひとつ前の文字を格納する。
        #都合のため1を格納しておく
        z="1"
        ts=0
        te=0
        u=[""]
        #48は24時間*2(30分毎なので)
        for j in range(48):
            #clは予定がない時間帯のある日を記録するためのlist
            #もし予定がない時間帯があるならclに格納。何日に予定があるかを示す。
            if o[j+2]=="0":
                cl[i]=i
            #zはlistのひとつ前の文字を格納している
            #今の文字と前の文字が
            #0,0なら終わりの時間を30分伸ばす
            if o[j+2]=="0" and z=="0":
                te=te+30*60
            #0,1なら初めの時間を記録し、終わりの時間をその30分後とする。
            elif o[j+2]=="0" and z=="1":
                ts=30*60*j
                te=ts+30*60
            #1,0なら初めの時間と終わりの時間をsからhやmに直して文字列としてuに格納する。
            elif o[j+2]=="1" and z=="0":
                ah=int(ts/(60*60))
                am=int((ts%(60*60))
                       /60)
                bh=int(te/(60*60))
                bm=int((te%(60*60))
                       /60)
                u.append(f'{ah:02}'+":"+f'{am:02}'+"~"+f'{bh:02}'+":"+f'{bm:02}')
            #1,1の場合は何もしない
            #もしteが86400秒(24時間)になったら
            #初めの時間と終わりの時間をsからhやmに直して文字列としてuに格納する。
            if te==86400:
                ah=int(ts/(60*60))
                am=int((ts%(60*60))
                       /60)
                bh=int(te/(60*60))
                bm=int((te%(60*60))
                       /60)
                u.append(f'{ah:02}'+":"+f'{am:02}'+"~"+f'{bh:02}'+":"+f'{bm:02}')
            #zに今回の文字を格納して次回へ
            z=o[j+2]
        #1日の空いてる時間帯の格納されたlistを日付と同じindexの配列RTへ格納する
        RT[i]=u

    return render_template('G_Schedule/frmGroupSchedule.html',
                           year=year,
                           month=month,
                           month_last_day=month_last_day,
                           day_upper_left=day_upper_left,
                           cl=cl,
                           RT=RT)

@app.route("/GSchedule/<int:year>-<int:month>-<int:d>")
##データベースからyear,month,d(date)のスケジュールがあるか、
def Gtimeline(year,month,d,user_id=0):

    year=year
    month=month
    d=d
    con=sqlite3.connect(MYDATABASE)
    cur=con.cursor()
    db_kyaku=cur.execute('SELECT * FROM kyaku WHERE user_id= '+ str(user_id)).fetchall()
    gpid=db_kyaku[0][3]
    k=cur.execute('SELECT * FROM kyaku WHERE gpid='+ str(gpid)).fetchall()
    db_schedule=[]
    for i in k:
        K=i[0]
        db_schedule.append(cur.execute('SELECT * FROM schedule WHERE year= '+ str(year) 
                                       +" AND month= "+ str(month) 
                                       +" AND date="+ str(d) 
                                       +" AND user_id="+ str(K)).fetchall())
    con.close()
    
    schedule_bit=list(format(Ctimeline(db_schedule, d), '#050b'))
    
    return render_template('/G_Schedule/Timeline.html',
                           year=year,
                           month=month,
                           d=d,
                           schedule_bit=schedule_bit)

def change_bit(start_time, end_time):
    
    date_bit = 0b0

    for i in range(48):
        #予定がある場合
        if start_time<= i*60*30 and i*60*30 <end_time:
            date_bit+=2**(47-i)
        #予定がない場合
        else:
            date_bit+=0
    
    return date_bit

def Ctimeline(db_schedule, d):
    schedule =[]
    for i in db_schedule:
        for row in i:
            #日付が指定された日(d)と同じなら
            if row[5]==d:
                schedule.append(row)

    schedule_bit=0
    for i in range(len(schedule)):
        schedule_bit=schedule_bit | change_bit(schedule[i][6],schedule[i][7])
    return schedule_bit


