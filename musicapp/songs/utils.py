import os
import secrets
from werkzeug.utils import secure_filename
from flask import current_app as app


def save_song(file):
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    _, f_ext = os.path.splitext(secure_filename(file.filename))
    random_hex = secrets.token_hex(8)
    filename = random_hex + f_ext
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    return filename
