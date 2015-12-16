from flask import Flask, url_for, render_template, request, url_for, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from auth import validate_login

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dayu.db'
db = SQLAlchemy(app)

@app.route('/')
def home():
    return 'hello world'

@app.route('/questions')
def questions():
    return 'hello questions'

@app.route('/questions/<int:qid>')
def question(qid):
    pass

@app.route('/answers')
def answers():
    pass

@app.route('/answers/<int:aid>')
def answer(aid):
    pass

@app.route('/user/login',methods=['GET','POST'])
def user_login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        if validate_login(request.form['username'], request.form['password']):
            return redirect(url_for('user_home'))
        else:
            return 'login failed'	

@app.route('/user/home')
def user_home():
    return render_template('user/home.html')

@app.route('/user/search',methods=['GET', 'POST'])
def user_search():
    return render_template('user/search.html')

@app.route('/user/<int:uid>/questions')
def questions_submitted_by(uid):
    pass

@app.route('/consultant/login',methods=['GET','POST'])
def consultant_login():
    pass

@app.route('/consultant/home')
def consultant_home():
    pass

@app.route('/consultant/<int:uid>/questions')
def asking_to(uid):
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0')
