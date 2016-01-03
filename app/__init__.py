#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Flask, render_template, redirect, request, session
from flask.ext.sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dayu.db'
app.secret_key = 'secret'
db = SQLAlchemy(app)
socketio = SocketIO(app)

@app.before_request
def before_any_request():
	path = request.path
    if not path.endswith('/login') and not path.endswith('/home') and '/static/' not in request.path:
        session['last_url'] = request.path

import controllers