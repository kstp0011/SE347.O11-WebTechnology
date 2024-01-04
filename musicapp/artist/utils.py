import os
import secrets
from werkzeug.utils import secure_filename
from flask import current_app as app
import requests
from PIL import Image
import io

# def save_image(file):
#     if not os.path.exists(app.config['UPLOAD_FOLDER_IMAGES']):
#         os.makedirs(app.config['UPLOAD_FOLDER_IMAGES'])
#     _, f_ext = os.path.splitext(secure_filename(file.filename))
#     random_hex = secrets.token_hex(8)
#     filename = random_hex + f_ext
#     file_path = os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], filename)
#     file.save(file_path)
#     return filename

def save_image(file):
    if not os.path.exists(app.config['UPLOAD_FOLDER_IMAGES']):
        os.makedirs(app.config['UPLOAD_FOLDER_IMAGES'])
    _, f_ext = os.path.splitext(secure_filename(file.filename))
    random_hex = secrets.token_hex(8)
    filename = random_hex + f_ext
    file_path = os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], filename)

    try:
        # Open the image file
        img = Image.open(file)
        width, height = img.size

        # Find dimensions for the square crop
        if width > height:
            left = (width - height) / 2
            top = 0
            right = (width + height) / 2
            bottom = height
        else:
            left = 0
            top = (height - width) / 2
            right = width
            bottom = (height + width) / 2

        # Crop the image
        img_cropped = img.crop((left, top, right, bottom))

        # Save the cropped image
        img_cropped.save(file_path)
    except:
        file.save(file_path)

    return filename

