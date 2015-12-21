#!/usr/bin/python
# -*- coding: UTF-8 -*-
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app import db

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

class Specialty(db.Model):
    __tablename__ = 'specialties'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    profiles = db.relationship('Profile', backref = db.backref('specialty'))
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
    specialty_id = Column(Integer, db.ForeignKey('specialties.id'))
    location_id = Column(Integer, db.ForeignKey('locations.id'))
    created_on = Column(DateTime, server_default=db.func.now())
    updated_on = Column(DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

class Category(db.Model):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    questions = db.relationship('Question', backref = db.backref('category'))
    def __str__(self):
        return self.name

class Question(db.Model):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    status = Column(Boolean, default=False)
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
    created_on = Column(DateTime, server_default=db.func.now())
    updated_on = Column(DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

def init_data():
       
    admin = Role(name='admin')
    consultant = Role(name='consultant')
    userRole = Role(name='user')
    
    shanghai = Location(name=u'上海')
    kunshan = Location(name=u'昆山')
    suzhou = Location(name=u'苏州')

    law = Specialty(name=u'法律')
    account = Specialty(name=u'会计')
    tax = Specialty(name=u'税务')

    user = User(name='falcon',password='falcon') 
    user.roles = [admin, consultant, userRole]
    profile = Profile(value=100)
    profile.location = shanghai
    profile.specialty = law
    user.profile = profile
    db.session.add(user)
    db.session.commit()

    consultant1 = User(name='c1',password='password')
    consultant1.roles = [consultant, userRole]
    profile2 = Profile(value=100)
    profile2.location = suzhou
    profile2.specialty = tax
    consultant1.profile = profile2
    db.session.add(consultant1)
    db.session.commit()

    user1 = User(name='u1',password='password')
    user1.roles = [userRole]
    account = Account(points = 100)
    user1.account = account
    db.session.add(user1)
    db.session.commit()
    


   

