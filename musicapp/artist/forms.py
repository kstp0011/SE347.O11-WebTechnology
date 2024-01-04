import os
from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired, ValidationError


class ArtistForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    birth_date = DateField('Birth Date', validators=[DataRequired()])
    image = FileField('Select an image: ', validators=[
                      DataRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Upload')

    def validate_image(self, image):
        if image.data:
            _, ext = os.path.splitext(image.data.filename)
            ext = ext.lower()
            if ext not in ['.jpg', '.png']:
                raise ValidationError('Only jpg and png files allowed.')

