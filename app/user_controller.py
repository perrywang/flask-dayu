#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import request, render_template, redirect, session
from sqlalchemy import and_, or_
from app import app, db
from auth import register_user, validate_login, auth_required, authenticated, has_role, current_user
from models import User, Profile, Category, Location


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
        if session['login_url'] == '/consultant/login' and has_role(['consultant','admin']):
            return redirect('/consultant/home')
        else:
            return redirect('/user/home')
    elif request.method == 'GET':
        return render_template('login.html', isConsultant = False)
    if request.method == 'POST':
        logging_user = validate_login(request.form['username'], request.form['password'])
        if logging_user is not None:
            session.permanent = True
            session['user'] = {'username':logging_user.name, 'uid':logging_user.id, 'roles':[role.name for role in logging_user.roles]}
            session['login_url'] = '/user/login'
            return redirect('/user/home')
        else:
            return 'login failed'


@app.route('/user/logout')
@auth_required()
def user_logout():
    current_user().status = 'offline'
    db.session.commit()
    session.pop('user', None)
    session.pop('login_url', None)
    return redirect('/user/login')


@app.route('/user/home')
@auth_required()
def user_home():
    return render_template('user/home.html')


@app.route('/user/search',methods=['GET', 'POST'])
@auth_required()
def user_search():
    if request.method == 'GET':
        locations = Location.query.all();
        categories = Category.query.all();
        return render_template('user/search.html', locations = locations, categories = categories)
    else:
        cat = request.form['category']
        loc = request.form['location']
        consultants = User.query.with_entities(User.id, User.status, Profile.desc, Profile.real_name, Profile.value).join(Profile).join(Category).join(Location).filter(and_(Location.name == loc, or_(Category.name == cat, Category.parent.has(name=cat)))).all()
        return render_template('user/consultlist.html',consultants=consultants)

@app.route('/user/<int:uid>/questions')
@auth_required()
def questions_submitted_by(uid):
    pass


@app.route('/user/online')
@auth_required()
def user_online():
    #user = User.query.get(session['user']['uid'])
    user = current_user()
    user.status = 'online'
    db.session.commit()
    return 'online'

@app.route('/user/offline')
@auth_required()
def user_offline():
    #user = User.query.get(session['user']['uid'])
    user = current_user();
    user.status = 'offline'
    db.session.commit()
    return 'offline'


