from flask import request, render_template, redirect, url_for
from app import app
from auth import validate_login

@app.route('/consultant/login',methods=['GET','POST'])
def consultant_login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        if validate_login(request.form['username'], request.form['password']):
            return render_template('consultant/home.html')
        else:
            return 'login failed'


@app.route('/consultant/home')
def consultant_home():
    return render_template('consultant/home.html')


@app.route('/consultant/<int:uid>/questions')
def asking_to(uid):
    pass