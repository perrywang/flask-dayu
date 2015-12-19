#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import request, render_template, redirect, url_for, session
from app import app
from auth import register_user, validate_login, auth_required, authenticated, has_role
from sqlalchemy import and_
from models import User, Profile


@app.route('/user/register',methods = ['GET','POST'])
def register():
    if authenticated() and (not has_role(['admin'])):
        return '请先注销当前登录'
    if request.method == 'GET':
        return render_template('register.html')
    else:
        registering_user = register_user(request.form['username'],request.form['password'])
        if registering_user is not None:
            if not 'user' in session:
                session.permanent = True
                session['user'] = {'username':registering_user.name, 'uid':registering_user.id, 'roles':[role.name for role in registering_user.roles]} 
                return redirect('/user/home')
            elif has_role(['admin']):
                return redirect('/user/register')
        else:
            return redirect('/user/register')

@app.route('/user/login',methods=['GET','POST'])
def user_login():
    if authenticated():
        return redirect('/user/home')
    elif request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        logging_user = validate_login(request.form['username'], request.form['password'])
        if logging_user is not None:
            session.permanent = True
            session['user'] = {'username':logging_user.name, 'uid':logging_user.id, 'roles':[role.name for role in logging_user.roles]}
            return redirect('/user/home')
        else:
            return 'login failed'


@app.route('/user/logout')
@auth_required
def user_logout():
    session.pop('user', None)
    return redirect('/user/login')


@app.route('/user/home')
@auth_required
def user_home():
    return render_template('user/home.html')


@app.route('/user/search',methods=['GET', 'POST'])
@auth_required
def user_search():
    if request.method == 'GET':
        return render_template('user/search.html')
    else:
        spec = request.form['specialty']
        loc = request.form['location']
        consultants = User.query.join(Profile).filter(Profile.specialty.has(name=spec),Profile.location.has(name=loc)).all()
        return render_template('user/consultlist.html',consultants=consultants)

@app.route('/user/<int:uid>/questions')
@auth_required
def questions_submitted_by(uid):
    pass