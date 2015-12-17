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

@app.route('/register',methods = ['GET','POST'])
def register():
    if authenticated():
        return '请先注销当前登录'
    if request.method == 'GET':
        return render_template('register.html')
    else:
        registering_user = register_user(request.form['username'],request.form['password'])
        if registering_user is not None:
            session.permanent = True
            session['user'] = {'username':registering_user.name, 'uid':registering_user.id, 'roles':[role.name for role in registering_user.roles]} 
            return redirect('/user/home')
        else:
            return redirect('/register')

import controllers