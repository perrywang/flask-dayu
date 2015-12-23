#!/usr/bin/python
# -*- coding: UTF-8 -*-
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app import db
import random

user_role = db.Table('user_role', db.Column('user_id', db.Integer, db.ForeignKey('users.id')), db.Column('role_id', db.Integer, db.ForeignKey('roles.id')))

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(50))
    status = Column(String(32), default='offline')
    created_on = Column(DateTime, server_default=db.func.now())
    updated_on = Column(DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    account = db.relationship('Account', backref = db.backref('user'), uselist = False)
    profile = db.relationship('Profile', backref = db.backref('user'), uselist = False)
    roles = db.relationship('Role', secondary=user_role, backref=db.backref('users', lazy='dynamic'))
    questions_submitted = db.relationship('Question', backref = db.backref('submitter'), lazy='dynamic', foreign_keys='Question.submitter_id')
    questions_to = db.relationship('Question', backref = db.backref('to'), lazy='dynamic', foreign_keys='Question.to_id')
    answers = db.relationship('Answer', backref = db.backref('by'), lazy='dynamic')
    def __str__(self):
        return self.name

class Account(db.Model):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, db.ForeignKey('users.id'))
    points = Column(Integer, default=0)
    created_on = Column(DateTime, server_default=db.func.now())
    updated_on = Column(DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

class Role(db.Model):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    def __str__(self):
        return self.name

class Location(db.Model):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    profiles = db.relationship('Profile', backref = db.backref('location'))
    def __str__(self):
        return self.name

class Profile(db.Model):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, db.ForeignKey('users.id'))
    value = Column(Integer)
    real_name = Column(String(32))
    desc = Column(String(512))
    mobile = Column(String(32))
    category_id = Column(Integer, db.ForeignKey('categories.id'))
    location_id = Column(Integer, db.ForeignKey('locations.id'))
    created_on = Column(DateTime, server_default=db.func.now())
    updated_on = Column(DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

class Category(db.Model):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, db.ForeignKey('categories.id'))
    name = Column(String(50), unique=True)
    questions = db.relationship('Question', backref = db.backref('category'), foreign_keys='Question.category_id')
    profiles = db.relationship('Profile', backref = db.backref('category'), foreign_keys = 'Profile.category_id')
    sub_categories = db.relationship('Category', backref=db.backref('parent', remote_side='Category.id'))
    def __str__(self):
        return self.name

class Question(db.Model):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    status = Column(Boolean, default=False)
    answer = db.relationship('Answer', backref = db.backref('question'), uselist=False)
    category_id = Column(Integer, db.ForeignKey('categories.id'))
    submitter_id = Column(Integer,db.ForeignKey('users.id'))
    to_id = Column(Integer,db.ForeignKey('users.id'))
    created_on = Column(DateTime, server_default=db.func.now())
    updated_on = Column(DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

class Answer(db.Model):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    feedback = Column(Boolean, default=True)
    by_id = Column(Integer, db.ForeignKey('users.id'))
    question_id = Column(Integer,db.ForeignKey('questions.id'))
    created_on = Column(DateTime, server_default=db.func.now())
    updated_on = Column(DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

def init_data():
       
    admin = Role(name='admin')
    consultant = Role(name='consultant')
    userRole = Role(name='user')

    shanghai = Location(name=u'上海')
    kunshan = Location(name=u'昆山')
    suzhou = Location(name=u'苏州')
    zhenjiang = Location(name=u'镇江')
    wuxi = Location(name=u'无锡')
    taizhou = Location(name=u'台州')
    hangzhou = Location(name=u'杭州')

    law = Category(name=u'法律')

    minfa = Category(name=u'民法', parent = law)
    xingfa = Category(name=u'刑法', parent = law)
    susongfa = Category(name=u'诉讼法', parent = law)

    account = Category(name=u'会计')
    tax = Category(name=u'税务')

    db.session.add(admin)
    db.session.add(consultant)
    db.session.add(userRole)
    db.session.add(shanghai)
    db.session.add(kunshan)
    db.session.add(suzhou)
    db.session.add(zhenjiang)
    db.session.add(wuxi)
    db.session.add(taizhou)
    db.session.add(hangzhou)
    db.session.add(law)
    db.session.add(account)
    db.session.add(tax)
    db.session.commit()

    locations = [shanghai, kunshan, suzhou, zhenjiang, wuxi, taizhou, hangzhou]

    categories = [law, minfa, xingfa, susongfa, account, tax]

    falcon = User(name='falcon',password='falcon')
    falcon.roles = [admin, consultant, userRole]
    db.session.add(admin)
    db.session.commit()

    levels = [u'殿堂级律师', u'资深律师', u'高级律师', u'中级律师', u'初级律师']

    values = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

    real_names = [u'管理员', u'张宏', u'徐峥', u'张鹏', u'李成浩', u'张华', u'徐宏', u'张峥', u'周鹏', u'高飞', u'张爱国']

    status = ['online', 'offline']

    for i in range(1, 11):
        c = User(name='c'+str(i), password = 'password')
        c.roles = [consultant, userRole]
        c.status = random.choice(status)
        profile = Profile()
        profile.value = random.choice(values)
        profile.location = random.choice(locations)
        profile.category = random.choice(categories)
        profile.desc = random.choice(levels)
        profile.real_name = real_names[i]
        c.profile = profile
        db.session.add(c)
        db.session.commit()

    points = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

    for i in range(1, 21):
        u = User(name='u'+str(i),password='password')
        u.roles = [userRole]
        account = Account()
        account.points = random.choice(points)
        u.account = account
        db.session.add(u)
        db.session.commit()


    


   

