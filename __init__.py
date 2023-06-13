from flask import Flask
app = Flask(__name__)
import SSS.main

from SSS import db
db.create_schedule_table()
