from app import app, db
from flask_admin import Admin
from app.models import User, Role, Location, Specialty, Profile
from flask_admin.contrib.sqla import ModelView

if __name__ == '__main__':
    
    app.debug = True
    admin = Admin(app,template_mode='bootstrap3')
    admin.add_view(ModelView(Role, db.session))
    admin.add_view(ModelView(Location, db.session))
    admin.add_view(ModelView(Specialty, db.session))
    admin.add_view(ModelView(Profile, db.session))
    admin.add_view(ModelView(User, db.session))
    app.run(host='0.0.0.0')
