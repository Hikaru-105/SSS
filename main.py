import schedule_system_database
import searchGroup, updateGroup
from flask import render_template, redirect, request, url_for

import datetime
import calendar

import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user

import random

from werkzeug.security import generate_password_hash, check_password_hash
import os

import re

from waitress import serve

schedule_system_database.create_schedule_table()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'instance', 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = os.urandom(24)

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.Integer, nullable=False, unique=False, primary_key=False)
    username = db.Column(db.String(16), nullable=False, unique=False, primary_key=False)
    password = db.Column(db.String(16))

login_manager = LoginManager()
login_manager.init_app(app)

with app.app_context():
    db.create_all()

#データベースファイルの位置
DATABASE = 'instance/database.db'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def isalnum_ascii(s):
    return True if s.isalnum() and s.isascii() else False


@app.route("/")
def to_login_page():
    return redirect(url_for('login'))

@app.route("/authenticated", methods=['GET', 'POST'])
@login_required
def schedule():
    if request.method == 'GET':
        posts  = User.query.all()
        current_user.id = f'{current_user.id:08}'
        today = datetime.datetime.now()
        return redirect(url_for('monthcalendar', year=today.year, month=today.month))

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        re_password = request.form.get('re_password')
        group = 0
        if(len(username) > 16):
            e = 'ユーザ名は16文字以内にしてください'
            return render_template('signup.html', e=e)
        if(len(password) > 16):
            e = 'パスワードは16文字以内にしてください'
            return render_template('signup.html', e=e)
        if(password!=re_password):
            e = 'パスワードと確認用パスワードが一致していません'
            return render_template('signup.html', e=e)
        if(isalnum_ascii(password) == False):
            e = 'パスワードは半角英数にしてください'
            return render_template('signup.html', e=e)
        user = User(username=username, password=generate_password_hash(password, method='sha256'), group=group)

        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('schedule'))
    else:
        return render_template('signup.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        hage = request.args.get('checkbox_sample', default='', type=str)
        if hage == 'on':
            return render_template('signup.html')
        id = request.form.get('id')
        password = request.form.get('password')

        if(User.query.filter_by(id=id).count()==0):
            e = 'IDが間違っています'
            return render_template('login.html', e=e)

        user = User.query.filter_by(id=id).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('schedule'))
        else:
            e = 'IDまたはパスワードが間違っています'
            return render_template('login.html', e=e)
    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


#月カレンダー表示
@app.route('/monthcalendar/<int:year>-<int:month>')
#ログイン要求
@login_required
#カレンダー表示
def monthcalendar(year, month):
    user_id = current_user.id
    group = current_user.group
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
        user_id = user_id,
        group = group,
        year = year,
        month = month,
        month_last_day = month_last_day,
        day_upper_left = day_upper_left
    )

#スケジュール編集する日付を選択
@app.route('/edit/<int:year>-<int:month>-<int:date>')
@login_required
def edit(year,month,date):
    #結合テストするときにログイン情報から取得
    user_id = current_user.id
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
@login_required
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
@login_required
def edit_weekday(year, month):
    #結合テストするときはログイン情報から取得
    user_id = current_user.id
    return render_template(
    'I_Schedule/weekdayedit.html',
    user_id = user_id,
    year = year,
    month = month,
    )

@app.route('/submit_weekday_schedule/<int:user_id>-<int:year>-<int:month>', methods=['POST'])
@login_required
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
        if end_time > 86400:
            end_time = 86400
        new_schedules.append((schedule_id, sche_name[i], user_id, years[i], months[i], dates[i], start_time, end_time))
    #登録処理へリストを渡す
    schedule_system_database.registar_schedule(new_schedules, delete_schedules)


@app.route('/makeGroup')
@login_required
def makeGroup():
    user_id = current_user.id
    group = current_user.group
    today = datetime.datetime.now()
    if group == 0:
        return render_template(
            'makeGroup/makeGroup.html',
            user_id = user_id,
            group = group,
            year=today.year,
            month=today.month
        )
    else:
        return render_template(
            'makeGroup/makeGroup_already_joined.html',
            year=today.year,
            month=today.month
        )



@app.route('/submit_new_group', methods=['POST'])
@login_required
def submit_new_group():
    today = datetime.datetime.now()
    leader = current_user.id
    group_name = request.form.get('group_name')
    keyword = request.form.get('keyword')
    group_id = 0
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT group_id FROM 'group' ORDER BY group_id")
    id_search = cur.fetchall()
    con.close()
    id_search = [x[0] for x in id_search]
    #スケジュールIDが既存のものと重複しないように生成し、スケジュールのタプルをリストに追加
    overlap = True
    while overlap:
        group_id = random.randint(0, 99999999)
        overlap = group_id in id_search
    new_group = (group_id, group_name, keyword, leader)
    schedule_system_database.registar_group(new_group, current_user.id)
    return redirect(url_for('Gcalendar', year=today.year, month=today.month))


#グループスケジュールの表示関連
@app.route("/GSchedule/<int:year>-<int:month>")
@login_required
#########################################################
###Functionname :Gcalendar()
###Designer     :村田晃琉
###Function     :カレンダーを表示するための
#                   年、月、月初めの曜日、月の最後の日にち
###Return       :
#########################################################
def Gcalendar(year,month):
    user_id=current_user.id
    year=year
    month=month
    month_first_day=datetime.datetime(year,month,1)
    day_upper_left=month_first_day.weekday()*-1
    if day_upper_left == -6:
        day_upper_left=1
    month_last_day=calendar.monthrange(year,month)[1]
    con=sqlite3.connect(DATABASE)
    cur=con.cursor()
    #user_id(最初から保持)でDBから条件を絞りgroup_idを取得
    group_id=current_user.group
    #group_idでDBから条件を絞りグループ全員のuser_idを配列kへ取得
    k=cur.execute('SELECT * FROM user WHERE "group"='+ str(group_id)).fetchall()
    group_name=cur.execute('SELECT group_name FROM "group" WHERE "group_id"='+ str(group_id)).fetchone()[0]
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
                           RT=RT,
                           user_id=user_id,
                           group_id=group_id,
                           group_name=group_name
                           )

@app.route("/GSchedule/<int:year>-<int:month>-<int:d>")
@login_required
##データベースからyear,month,d(date)のスケジュールがあるか、
def Gtimeline(year,month,d):
    user_id=current_user.id
    year=year
    month=month
    d=d
    con=sqlite3.connect(DATABASE)
    cur=con.cursor()
    group_id=current_user.group
    k=cur.execute('SELECT * FROM user WHERE "group" = '+ str(group_id)).fetchall()
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

@login_required
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

@login_required
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

#グループ参加関連

###################################################################################################
# Function Name...joinGroupUI
# Designer........越村太一
# Modifier........渡邉優太
# Function........グループ名、合言葉の入力を受け取り認証要求をする
# Return..........userInput == "True" : 認証要求
#                 else                : グループ加入画面を表示する
###################################################################################################
@app.route("/joinGroup", methods=["GET", "POST"])  # @join.route("/joinGroup")
def joinGroupUI():
    today = datetime.datetime.now()
    c_group_id = current_user.group
    if request.method == "GET":
        group_id = ""
        keyword = ""
        url = "joinGroup/joinGroup.html"

    if request.method == "POST":
        group_id = int(request.form.get("group_id"))
        keyword = request.form.get("keyword")
        if group_id == "" or keyword == "":
            url = "joinGroup/joinGroup.html"
        else:
            userInput = request.form.get("userInput")
            if userInput == "True":
                return redirect(url_for("joinGroupAuth", group_id=group_id, keyword=keyword))
            elif userInput == "False":
                url = "joinGroup/joinGroup.html"

    return render_template(url, group_id=group_id, keyword=keyword, c_group_id=c_group_id, year=today.year, month=today.month, notExist="")


###################################################################################################
# Function Name...joinGroupAuth
# Designer........越村太一
# Function........グループ名、合言葉をsearchGroupへ渡し、返り値によって加入するか判定する
# Return..........searchGroupの返り値が0 : グループ加入画面を表示する
#                 else                   : グループスケジュール画面表示する
###################################################################################################
@app.route("/joinGroup/auth/<int:group_id>/<string:keyword>")
def joinGroupAuth(group_id, keyword):
    today = datetime.datetime.now()
    c_group_id = current_user.group
    existence = searchGroup.searchGroup(group_id, keyword)
    if not existence:
        url = "joinGroup/joinGroup.html"
        script = "<script>alert('入力されたグループは見つかりませんでした');</script>"
        return render_template(url, group_id=group_id, keyword=keyword, c_group_id=c_group_id, year=today.year, month=today.month, notExist=script)
    else:
        user_id = current_user.id
        updateGroup.updateGroup(user_id, group_id)
        today = datetime.datetime.now()
        return redirect(url_for('Gcalendar', year=today.year, month=today.month))



if __name__ == "__main__":
    #app.run('0.0.0.0',port=5000)
    serve(app, host='0.0.0.0', port=51080)
