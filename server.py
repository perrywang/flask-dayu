from app import app, socketio
from app.admin import start_admin

if __name__ == '__main__':
    app.debug = True
    start_admin(app)
    socketio.run(app,host='0.0.0.0')
