from app import app

@app.route('/questions')
def questions():
    pass

@app.route('/questions/<int:qid>')
def question(qid):
    pass

@app.route('/answers')
def answers():
    pass

@app.route('/answers/<int:aid>')
def answer(aid):
    pass

@app.route('/usre/login',methods=['GET','POST'])
def user_login():
    pass

@app.route('/user/home')
def user_home():
    pass

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