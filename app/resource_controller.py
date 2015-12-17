from app import app

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
