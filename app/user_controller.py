from flask import request, render_template, redirect, url_for
from app import app
from auth import validate_login

@app.route('/user/login',methods=['GET','POST'])
def user_login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        if validate_login(request.form['username'], request.form['password']):
            return render_template('user/home.html')
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