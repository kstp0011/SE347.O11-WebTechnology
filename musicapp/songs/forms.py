import os
from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class SongForm(FlaskForm):
    song = FileField('Select an MP3 file: ', validators=[
                     DataRequired(), FileAllowed(['mp3'], 'mp3 files only!')])
    submit = SubmitField('Upload')

    def validate_song(self, song):
        if song.data:
            _, ext = os.path.splitext(song.data.filename)
            ext = ext.lower()
            if ext != '.mp3':
                raise ValidationError('Only mp3 files allowed.')

            if song.data.content_length > current_app.config['MAX_CONTENT_LENGTH']:
                raise ValidationError(
                    'Song size too large! Upload songs of size less than 20MB.')


class SongMetadataForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    artist = StringField('Artist', validators=[DataRequired()])
    album = StringField('Album', validators=[DataRequired()])
    submit = SubmitField('Save Song')


class SearchForm(FlaskForm):
    search_input_text = StringField(
        'What you want to listend to..?', validators=[DataRequired()])
    submit = SubmitField('Search')


class CommentForm(FlaskForm):
    comment = StringField('Comment', validators=[DataRequired()])
    submit = SubmitField('Comment')


class ReplyForm(FlaskForm):
    reply = StringField('Reply', validators=[DataRequired()])
    submit = SubmitField('Reply')


class PlaylistForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Create Playlist')
