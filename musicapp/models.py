import jwt
from time import time
from flask_login import UserMixin
from flask import current_app as app
from musicapp import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    songs = db.relationship('Song', backref='owner', lazy=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_manager = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}')"

    def get_reset_token(self, expires_sec=1800):
        return jwt.encode({'user_id': self.id, 'exp': time() + expires_sec}, key=app.config['SECRET_KEY'])

    @staticmethod
    def verify_reset_token(token):
        try:
            user_id = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms=['HS256'])[
                'user_id']
        except:
            return None
        return User.query.get(user_id)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    artist = db.Column(db.String(50), nullable=False)
    album = db.Column(db.String(50))
    filename = db.Column(db.String(150), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist_info.id'))
    date_uploaded = db.Column(db.DateTime, nullable=False,
                              default=db.func.current_timestamp())
    likes = db.relationship('Like', backref='song', lazy='dynamic')
    artist_info = db.relationship(
        'Artist_info', backref=db.backref('songs', lazy=True))

    # in development
    # genre = db.Column(db.String(50))
    # cover = db.Column(db.String(150))

    def __repr__(self) -> str:
        return f"Song('{self.title}', '{self.artist}', '{self.album}', '{self.filename}', '{self.owner_id}', '{self.artist_id}', '{self.date_uploaded}, '{self.likes}')"


class Artist_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    image = db.Column(db.String(150))

    def __repr__(self) -> str:
        return f"Artist_info('{self.name}', '{self.image}')"

# interactions


class Like(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), primary_key=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'))


class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
