from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from musicapp.config import Config


mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from musicapp.users.routes import users
    from musicapp.songs.routes import songs
    from musicapp.main.routes import main
    from musicapp.errors.handlers import errors
    from musicapp.artist.routes import artists
    app.register_blueprint(users)
    app.register_blueprint(songs)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(artists)

    return app
