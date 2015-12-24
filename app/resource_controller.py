from flask import render_template, request, session, redirect
from models import User, Question, Answer
from app import app, db, socketio
from auth import auth_required, current_user

@app.route('/questions/new')
def new_question():
    cid = request.args.get('to', '')
    consultant = None
    if not cid == '':
        consultant = User.query.get(int(cid))
        return render_template('user/questioning.html', to=consultant, question=None)

@app.route('/quick/new')
def quick_new_question():
    return render_template('user/quickquestioning.html', question=None)

@app.route('/quick/create')
def quick_create_question():
    pass

@app.route('/questions/<int:qid>/edit',methods=['GET','POST'])
def edit_question(qid):
    question = Question.query.get(qid)
    if request.method == 'GET':
        return render_template('user/questioning.html', question = question, to=question.to)
    else:
        question.description = request.form['description']
        db.session.commit()
        return redirect('/questions/by/' + str(current_user().id))

@app.route('/questions/create', methods=['POST'])
@auth_required
def create_question():
    toid = request.args.get('to', '')
    if not toid == '':
        question = Question(submitter_id=session['user']['uid'], to_id=int(toid), description=request.form['description'])
        db.session.add(question)
        db.session.commit()
        socketio.emit('question_added', 'question created', room='consultants', namespace='/consultants')
        return redirect('/questions/by/'+str(current_user().id))

@app.route('/questions')
def questions():
    status = request.args.get('status','all')
    if status == 'all':
        questions = Question.query.all()
    elif status == 'answered':
        questions = Question.query.filter(Question.answer != None).all()
    else:
        questions = Question.query.filter(Question.answer == None).all()

    return render_template('consultant/consultant_questionlist.html',questions=questions)

@app.route('/questions/by/<int:uid>')
def questions_by(uid):
    status = request.args.get('status','all')
    if status == 'all':
        questions = User.query.get(uid).questions_submitted.all()
    elif status == 'answered':
        questions = User.query.get(uid).questions_submitted.filter(Question.answer != None).all()
    else:
        questions = User.query.get(uid).questions_submitted.filter(Question.answer == None).all()
    for question in questions:
        app.logger.info(question.description)
    return render_template('user/user_questionlist.html',questions=questions)

@app.route('/questions/to/<int:uid>')
def questions_to(uid):
    status = request.args.get('status','all')
    if status == 'all':
        questions = User.query.get(uid).questions_to.all()
    elif status == 'answered':
        questions = User.query.get(uid).questions_to.filter(Question.answer != None).all()
    else:
        questions = User.query.get(uid).questions_to.filter(Question.answer == None).all()
    
    return render_template('consultant/consultant_questionlist.html',questions=questions)

@app.route('/questions/<int:qid>')
def question(qid):
    pass

@app.route('/answers/for/<int:qid>',methods=['GET','POST'])
def answer_for(qid):
    question = Question.query.get(qid)
    if request.method == 'GET':
        return render_template('consultant/answering.html',question=question)
    else:
        if question.answer == None:
            answer = Answer(question_id=qid, by_id=current_user().id, description = request.form['answer'])
            db.session.add(answer)
            db.session.commit()
        else:
            question.answer.description = request.form['answer']
            db.session.commit()
        return redirect('/questions?status=no')


@app.route('/answers/me',methods=['GET'])
def answer_by():
    uid = current_user().id
    questions = Question.query.join(Answer).filter(Answer.by_id == uid).all()
    return render_template('consultant/consultant_questionlist.html',questions=questions)

@app.route('/answers/<int:aid>')
def answer(aid):
    pass
