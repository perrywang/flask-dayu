from flask_socketio import emit, send, join_room
from app import app, socketio

@socketio.on('answer_added', namespace='/users')
def handle_user_event(json):
    pass


@socketio.on('join', namespace='/consultants')
def join_consultant_room(json):
    app.logger.info('received join request')
    join_room('consultants')
    emit('joined', 'joined successfully')

@socketio.on('question_added', namespace='/consultants')
def broadcast_question_added(json):
    pass



