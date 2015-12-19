from app import db
from models import init_data

def init_db():
    db.drop_all()
    db.create_all()
    init_data()


