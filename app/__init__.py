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

@app.errorhandler(500)
def all_exception_handler(error):
    return redirect('/user/logout')

@app.errorhandler(401)
def no_authorization_handler(error):
    return redirect(session['last_url'])

@app.after_request
def after_any_request(response):
    path = request.path
    if request.method == 'GET' and '/static/' not in path:
        if request.query_string is not None:
            path = path + '?' + request.query_string
        session['last_url'] = path
    return response

import controllers
