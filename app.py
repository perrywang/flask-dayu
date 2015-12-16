from flask import Flask, url_for
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dayu.db'
db = SQLAlchemy(app)

import routes

if __name__ == '__main__':
    app.run()
