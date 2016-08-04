# Consulting system based Flask framework for weixin platform

## Core concepts
**Role** admin, consultant, user  
**Real time** WebSocket support  
**Dashboard** Basic chart support

## Build
    git clone https://github.com/perrywang/flask-dayu.git
    cd flask-dayu
    pip install -r requirements.txt
    python
    >>>from app.database import init_db
    >>>init_db()
    python server.py
    visit localhost:5000/user/login, /consultant/login, /admin to access website
