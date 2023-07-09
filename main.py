# from SSS import app
from flask import render_template
import datetime
import calendar
import sqlite3
MYDATABASE='database.db'
    
def Gtimeline(year,month,d):

    year=year
    month=month
    d=d
    con=sqlite3.connect(MYDATABASE)
    cur=con.cursor()
    db_schedule=cur.execute('SELECT * FROM schedule WHERE year= '+ str(year) +" AND month= "+ str(month)+" AND date= "+ str(d)).fetchall()
    con.close()
    
    schedule = []
    for row in db_schedule:
        schedule.append(row)
    
    schedule_bit=0
    for i in range(1):
        schedule_bit=schedule_bit | change_bit(30*60*29,30*60*8)
    
    return print(format(schedule_bit, '#050b'))

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

def main():
    Gtimeline(2023,6,1)


if __name__=="__main__":
    main()
