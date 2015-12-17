from flask import request, render_template, redirect, url_for, session
from app import app
from auth import validate_login, authenticated, role_required

@app.route('/consultant/login',methods=['GET','POST'])
def consultant_login():
    if authenticated():
        return redirect('/consultant/home')
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        if validate_login(request.form['username'], request.form['password']):
            return redirect('/consultant/home')
        else:
            abort(401)

@app.route('/consultant/logout')
def consultant_logout():
    session.pop('user', None)
    return redirect('/consultant/login')

@app.route('/consultant/home')
@role_required(roles=['consultant','admin'])
def consultant_home():
    return render_template('consultant/home.html')


@app.route('/consultant/<int:uid>/questions')
def asking_to(uid):
    pass