from flask import render_template, request, session, redirect
from models import User, Question
from app import app, db
from auth import auth_required


@app.route('/questions/new')
def new_question():
    cid = request.args.get('to', '')
    if not cid == '':
        consultant = User.query.get(int(cid))
        return render_template('user/questioning.html', to=consultant)


@app.route('/questions/create', methods=['POST'])
@auth_required
def create_question():
    cid = request.args.get('to', '')
    if not cid == '':
        question = Question(submitter_id=session['user']['uid'], to_id=int(cid), description=request.form['description'])
        db.session.commit()
        return redirect('user/search')

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
