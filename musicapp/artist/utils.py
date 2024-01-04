import os
import secrets
from werkzeug.utils import secure_filename
from flask import current_app as app
import requests

def save_image(file):
    if not os.path.exists(app.config['UPLOAD_FOLDER_IMAGES']):
        os.makedirs(app.config['UPLOAD_FOLDER_IMAGES'])
    _, f_ext = os.path.splitext(secure_filename(file.filename))
    random_hex = secrets.token_hex(8)
    filename = random_hex + f_ext
    file_path = os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], 'Images', filename)
    file.save(file_path)
    return filename