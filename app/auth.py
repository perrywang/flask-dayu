#!/usr/bin/python
# -*- coding: UTF-8 -*-
from functools import wraps
from flask import redirect, request, session, abort
from app import db
from models import User, Role, Profile, Category, Location


def auth_required(redirect_url='/user/login'):
    def decorate(func):
        redirectPage = redirect_url   
        @wraps(func)
        def wrapper(*args, **kargs):
            if authenticated():
                return func(*args, **kargs)
            else:
                return redirect(redirectPage)
        return wrapper
    return decorate


def role_required(roles=['user']):
    def decorate(func):
        required_roles = roles

        @wraps(func)
        def wrapper(*args, **kargs):
            if authenticated() and has_role(required_roles):
                return func(*args, **kargs)
            else:
                return abort(401)
                
        return wrapper

    return decorate


def register_user(username, password):
    user = User(name=username, password=password)
    user.roles = [Role.query.filter_by(name='user').first()]
    db.session.add(user)
    db.session.commit()
    return user


def register_consultant(username, password, category, location, value):
    consultant = User(name=username, password=password)
    consultant.roles = [Role.query.filter_by(name='user').first(), Role.query.filter_by(name='consultant').first()]
    profile = Profile(category=Category.query.filter_by(name=category).first(),
                      location=Location.query.filter_by(name=location).first(), value=int(value))
    consultant.profile = profile
    db.session.add(consultant)
    db.session.commit()
    return register_consultant


def validate_login(username, password):
    user = User.query.filter_by(name=username).first()
    if user.password == password:
        user.status = 'online'
        db.session.commit()
        return user
    else:
        abort(401)


def authenticated():
    return ('user' in session) and (User.query.get(session['user']['uid']) is not None)


def has_role(required_roles):
    if not 'user' in session:
        return False
    roles = session['user']['roles']
    for role in roles:
        if role in required_roles:
            return True
    return False


def current_user():
    return User.query.get(session['user']['uid'])
