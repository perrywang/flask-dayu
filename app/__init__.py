#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Flask, render_template, redirect, request, session
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dayu.db'
app.secret_key = 'secret'
db = SQLAlchemy(app)

from auth import register_user, authenticated

@app.route('/')
def home():
    return 'hello dayu'



import controllers