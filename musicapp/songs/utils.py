import os
import secrets
from werkzeug.utils import secure_filename
from flask import current_app as app
import requests
# from musicapp.config import config


def save_song(file):
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    _, f_ext = os.path.splitext(secure_filename(file.filename))
    random_hex = secrets.token_hex(8)
    filename = random_hex + f_ext
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    return filename


def search_music(query):
    data = {
        'url': query,
        'return': 'apple_music,spotify',
        # Replace 'test' with your actual API token
        'api_token': '4975ba04425b8788ff0ba2cce9e1f31e'
    }

    result = requests.post('https://api.audd.io/', data=data)

    return result.json()
