from app import db
from models import User, Role, Location, Specialty, Profile, Account
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

class UserView(ModelView):
	form_excluded_columns = ['profile','account','questions', 'answers', 'created_on', 'updated_on']

class ProfileView(ModelView):
	form_excluded_columns = ['created_on', 'updated_on']

class AccountView(ModelView):
	form_excluded_columns = ['created_on', 'updated_on']

def start_admin(app):
    admin = Admin(app, template_mode='bootstrap3')   
    admin.add_view(ModelView(Location, db.session))
    admin.add_view(ModelView(Specialty, db.session))
    admin.add_view(ModelView(Role, db.session))
    admin.add_view(UserView(User, db.session))
    admin.add_view(AccountView(Account, db.session))
    admin.add_view(ProfileView(Profile, db.session))
    
