from app import db

def init_db():
    import models
    db.create_all()
