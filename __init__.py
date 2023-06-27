from flask import Flask
import os
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///user.db'
app.config["SECRET_KEY"] = os.urandom(24)
import SSS.login

from SSS import app