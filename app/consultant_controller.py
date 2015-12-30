from flask import request, render_template, redirect, url_for, session, abort
from app import app,db
from auth import validate_login, authenticated, auth_required, role_required, register_consultant, current_user, has_role


@app.route('/consultant/register',methods = ['GET','POST'])
@role_required(roles=['admin'])
def consultant_register():
    if request.method == 'GET':
        return render_template('consultant_register.html')
    else:
        registering_user = register_consultant(request.form['username'],request.form['password'],request.form['speciality'],request.form['location'], request.form['value'])
        if registering_user is not None:
            return redirect('/consultant/register')
        else:
            return redirect('/consultant/register')

@app.route('/consultant/login',methods=['GET','POST'])
def consultant_login():
    if authenticated():
        if session['login_url'] == '/consultant/login' and has_role(['consultant','admin']):
            return redirect('/consultant/home')
        else:
            return redirect('/user/home')
    if request.method == 'GET':
        return render_template('login.html',isConsultant = True)
    if request.method == 'POST':
        logging_user = validate_login(request.form['username'], request.form['password'])
        if logging_user is not None:
            session.permanent = True
            session['user'] = {'username':logging_user.name, 'uid':logging_user.id, 'roles':[role.name for role in logging_user.roles]}
            session['login_url'] = '/consultant/login'
            if has_role(['consultant','admin']):
                return redirect('/consultant/home')
            else:
                return redirect('/user/home')
        else:
            abort(401)

@app.route('/consultant/logout')
@role_required(roles=['consultant','admin'])
def consultant_logout():
    user = current_user()
    user.status = 'offline'
    db.session.commit()
    session.pop('user', None)
    session.pop('login_url', None)
    return redirect('/consultant/login')

@app.route('/consultant/home')
@auth_required
@role_required(roles=['consultant','admin'])
def consultant_home():
    return render_template('consultant/home.html')


@app.route('/consultant/<int:uid>/questions')
def asking_to(uid):
    pass
