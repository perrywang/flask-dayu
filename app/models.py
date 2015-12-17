from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app import db

user_role = db.Table('user_role', db.Column('user_id', db.Integer, db.ForeignKey('users.id')), db.Column('role_id', db.Integer, db.ForeignKey('roles.id')))

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(50))
    created_on = Column(DateTime, server_default=db.func.now())
    updated_on = Column(DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    account = db.relationship('Account', backref = db.backref('user'), uselist = False)
    profile = db.relationship('Profile', backref = db.backref('user'), uselist = False)
    roles = db.relationship('Role', secondary=user_role, backref=db.backref('users', lazy='dynamic'))
    questions = db.relationship('Question', backref = db.backref('submitter'), lazy='dynamic')
    answers = db.relationship('Answer', backref = db.backref('by'), lazy='dynamic')

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

class Specialty(db.Model):
    __tablename__ = 'specialties'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    profiles = db.relationship('Profile', backref = db.backref('specialty'))

class Location(db.Model):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    profiles = db.relationship('Profile', backref = db.backref('location'))

class Profile(db.Model):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, db.ForeignKey('users.id'))
    value = Column(Integer)
    specialty_id = Column(Integer, db.ForeignKey('specialties.id'))
    location_id = Column(Integer, db.ForeignKey('locations.id'))
    created_on = Column(DateTime, server_default=db.func.now())
    updated_on = Column(DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

class Category(db.Model):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    questions = db.relationship('Question', backref = db.backref('category'))

class Question(db.Model):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    status = Column(Boolean, default=False)
    category_id = Column(Integer, db.ForeignKey('categories.id'))
    submitter_id = Column(Integer,db.ForeignKey('users.id'))
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
