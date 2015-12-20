from app import app
from app.admin import start_admin

if __name__ == '__main__':
    app.debug = True
    start_admin(app)
    app.run(host='0.0.0.0')
