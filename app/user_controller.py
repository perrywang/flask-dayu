from flask import request, render_template, redirect, url_for, session
from app import app
from auth import validate_login, auth_required, authenticated

@app.route('/user/login',methods=['GET','POST'])
def user_login():
    if authenticated():
        return redirect('/user/home')
    elif request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        logging_user = validate_login(request.form['username'], request.form['password'])
        if logging_user is not None:
            session['user'] = {'username':logging_user.name, 'uid':logging_user.id, 'roles':[role.name for role in logging_user.roles]}
            return redirect('/user/home')
        else:
            return 'login failed'


@app.route('/user/logout')
def user_logout():
    session.pop('user', None)
    return redirect('/user/login')


@app.route('/user/home')
@auth_required
def user_home():
    return render_template('user/home.html')


@app.route('/user/search',methods=['GET', 'POST'])
@auth_required
def user_search():
    return render_template('user/search.html')

@app.route('/user/<int:uid>/questions')
@auth_required
def questions_submitted_by(uid):
    pass