from functools import wraps
from flask import redirect, request, session
from app import db
from models import User, Role

def auth_required(func):
	@wraps(func)
	def wrapper(*args,**kargs):
		if authenticated():
			return func(*args,**kargs)
		elif request.path.startswith('/user'):
			return redirect('/user/login')
		elif request.path.startswith('/consultant'):
			return redirect('/consultant/login')
		else:
			return redirect('/')
	return wrapper

def role_required(roles=['user']):
	def decorate(func):
		required_roles = roles
		@wraps(func)
		def wrapper(*args,**kargs):
			if has_role(required_roles):
				return func(*args,**kargs)
			else:
				return 'Authorization Error'
		return wrapper

	return decorate
		
def register_user(username, password):
	user = User(name=username, password=password)
	user.roles = [Role.query.get(1)]
	db.session.add(user)
	db.session.commit()
	return user

def validate_login(username, password):
	user = User.query.filter_by(name=username).first()
	if user.password == password:
		return user
	else:
		abort(401)

def authenticated():
	return 'user' in session

def has_role(required_roles):
	if not 'user' in session:
		return False	
	roles = session['user']['roles']
	for role in roles:
		if role in required_roles:
			return True
	return False
    
