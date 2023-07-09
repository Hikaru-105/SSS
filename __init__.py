from flask import Flask
app = Flask(__name__)
import SSS.main
import flask_sqlalchemy

from SSS import schedule_system_database
schedule_system_database.create_schedule_table()
