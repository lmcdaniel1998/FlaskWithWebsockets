from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

from flask_bootstrap import Bootstrap

from flask_socketio import SocketIO, send, emit, join_room, leave_room, \
    Namespace, disconnect

from flask_session import Session

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

bootstrap = Bootstrap(app)

app.config['SESSION_TYPE'] = 'filesystem'

# flask-socketio
socketio = SocketIO(app, cors_allowed_origins="*", manage_session=True) #, logger=True, engineio_logger=True)

from app import routes, models

