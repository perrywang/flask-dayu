from app import db
from models import User, Role, Location, Profile, Account, Category
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


class LocationView(ModelView):
    can_export = True

class RoleView(ModelView):
    can_export = True

class UserView(ModelView):
    can_export = True
    form_excluded_columns = ['profile','account','questions', 'answers', 'created_on', 'updated_on', 'questions_submitted', 'questions_to']

class ProfileView(ModelView):
    can_export = True
    form_excluded_columns = ['created_on', 'updated_on']

class CategoryView(ModelView):
    can_export = True
    form_excluded_columns = ['questions', 'profiles', 'created_on', 'updated_on', 'sub_categories']

class AccountView(ModelView):
    can_export = True
    form_excluded_columns = ['created_on', 'updated_on']

def start_admin(app):
    admin = Admin(app, template_mode='bootstrap3')   
    admin.add_view(LocationView(Location, db.session))
    admin.add_view(CategoryView(Category, db.session))
    admin.add_view(RoleView(Role, db.session))
    admin.add_view(UserView(User, db.session))
    admin.add_view(AccountView(Account, db.session))
    admin.add_view(ProfileView(Profile, db.session))
    
