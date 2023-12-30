import os
from musicapp.creds import SECRET_KEY, MAIL_PASSWORD, MAIL_USERNAME
# from pyngrok import ngrok


class Config:
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = os.path.join(
        os.getcwd(), 'musicapp/static/uploads')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = MAIL_USERNAME
    MAIL_PASSWORD = MAIL_PASSWORD
    # BASE_URL = ngrok.connect(5000).public_url
