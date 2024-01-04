import requests
from flask import request, jsonify
import os
from flask import render_template, url_for, flash, redirect, request, send_file, abort, Blueprint, request, current_app as app
from flask_login import current_user, login_required
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
import eyed3

from musicapp.models import Song, Artist_info, User, Like, Comment, Reply
from musicapp import db
from musicapp.songs.forms import SongForm, SearchForm, SongMetadataForm, CommentForm, ReplyForm
from musicapp.songs.utils import save_song, search_music

import requests

songs = Blueprint('songs', __name__)


@songs.context_processor
def layout():
    form = SearchForm()
    return dict(form=form)


@songs.route('/song/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = SongForm()
    if form.validate_on_submit():
        song_file = form.song.data
        filename = save_song(song_file)
        file_path = os.path.join(
            app.config['UPLOAD_FOLDER'], filename)
        audio = eyed3.load(file_path)
        title = audio.tag.title if audio.tag.title else "Unknown Title"
        artist = audio.tag.artist if audio.tag.artist else "Unknown Artist"
        album = audio.tag.album if audio.tag.album else "Unknown Album"
        song = Song(title=title, artist=artist,
                    album=album, owner=current_user, filename=filename)
        db.session.add(song)
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            os.remove(file_path)
            flash('Error uploading song, retry', 'danger')
            return redirect(url_for('songs.upload'))
        return redirect(url_for('songs.song_metadata', id=song.id))
    return render_template('upload_song.html', title='Upload Song', form=form)


# @songs.route('/song/upload/metadata/<int:id>', methods=['GET', 'POST'])
# @login_required
# def song_metadata(id):
#     form = SongMetadataForm()
#     song = Song.query.get_or_404(id)
#     if song.owner != current_user:
#         abort(403)

#     if form.validate_on_submit():
#         song.title = form.title.data
#         song.artist = form.artist.data
#         song.album = form.album.data
#         db.session.commit()

#         song_path = os.path.join(
#             app.root_path, app.config['UPLOAD_FOLDER'], song.filename)
#         audio = eyed3.load(song_path)
#         audio.tag.title = song.title
#         audio.tag.artist = song.artist
#         audio.tag.album = song.album
#         audio.tag.save()

#         flash(f'Song `{form.title.data}` has been uploaded!', 'success')
#         return redirect(url_for('songs.upload'))
#     elif request.method == 'GET':
#         form.title.data = song.title
#         form.artist.data = song.artist
#         form.album.data = song.album
#     return render_template('song_metadata.html', title='Edit song details', form=form)

# @songs.route('/song/upload/metadata/<int:id>', methods=['GET', 'POST'])
# @login_required
# def song_metadata(id):
#     form = SongMetadataForm()
#     song = Song.query.get_or_404(id)
#     if song.owner != current_user:
#         abort(403)

#     if form.validate_on_submit():
#         title = form.title.data if form.title.data else "Unknown Title"
#         artist = form.artist.data if form.artist.data else "Unknown Artist"
#         album = form.album.data if form.album.data else "Unknown Album"

#         if title == "Unknown Title" or artist == "Unknown Artist" or album == "Unknown Album":
#             song_path = os.path.join(
#                 app.root_path, app.config['UPLOAD_FOLDER'], song.filename)
#             os.remove(song_path)  # delete the file
#             db.session.delete(song)  # delete the song record
#             db.session.commit()
#             flash('Please provide a title, artist, and album.', 'danger')
#             return redirect(url_for('songs.upload'))
#         else:
#             song.title = title
#             song.artist = artist
#             song.album = album
#             db.session.commit()

#             song_path = os.path.join(
#                 app.root_path, app.config['UPLOAD_FOLDER'], song.filename)
#             audio = eyed3.load(song_path)
#             audio.tag.title = title
#             audio.tag.artist = artist
#             audio.tag.album = album
#             audio.tag.save()

#             flash(f'Song `{title}` has been uploaded!', 'success')
#             return redirect(url_for('songs.upload'))
#     elif request.method == 'GET':
#         form.title.data = song.title
#         form.artist.data = song.artist
#         form.album.data = song.album
#     return render_template('song_metadata.html', title='Edit song details', form=form)

@songs.route('/song/upload/metadata/<int:id>', methods=['GET', 'POST'])
@login_required
def song_metadata(id):
    form = SongMetadataForm()
    song = Song.query.get_or_404(id)
    if song.owner != current_user:
        abort(403)

    if form.validate_on_submit():
        title = form.title.data if form.title.data else "Unknown Title"
        artist_name = form.artist.data if form.artist.data else "Unknown Artist"
        album = form.album.data if form.album.data else "Unknown Album"

        if title == "Unknown Title" or artist_name == "Unknown Artist" or album == "Unknown Album":
            song_path = os.path.join(
                app.root_path, app.config['UPLOAD_FOLDER'], song.filename)
            os.remove(song_path)  # delete the file
            db.session.delete(song)  # delete the song record
            db.session.commit()
            flash('Please provide a title, artist, and album.', 'danger')
            return redirect(url_for('songs.upload'))
        else:
            artist_info = Artist_info.query.filter_by(name=artist_name).first()

            # If the artist doesn't exist, create a new Artist_info
            if artist_info is None:
                artist_info = Artist_info(name=artist_name)
                db.session.add(artist_info)
                db.session.commit()

            song.title = title
            song.artist = artist_name
            song.artist_id = artist_info.id  # set the artist_id to the id of the artist_info
            song.album = album
            db.session.commit()

            song_path = os.path.join(
                app.root_path, app.config['UPLOAD_FOLDER'], song.filename)
            audio = eyed3.load(song_path)
            audio.tag.title = title
            audio.tag.artist = artist_name
            audio.tag.album = album
            audio.tag.save()

            flash(f'Song `{title}` has been uploaded!', 'success')
            return redirect(url_for('songs.upload'))
    elif request.method == 'GET':
        form.title.data = song.title
        form.artist.data = song.artist  # get the name of the artist
        form.album.data = song.album
    return render_template('song_metadata.html', title='Edit song details', form=form)


# @songs.route('/song/play/<int:song_id>')
# @login_required
# def song(song_id):
#     song = Song.query.get_or_404(song_id)
#     song_file = url_for('static', filename='uploads/' + song.filename)
#     songs = Song.query.order_by(Song.id).all()
#     next_song = Song.query.filter(Song.id > song_id).first()
#     prev_song = Song.query.filter(
#         Song.id < song_id).order_by(Song.id.desc()).first()
#     return render_template('song.html', song=song, music=song_file, songs=songs, next_song=next_song, prev_song=prev_song)

@songs.route('/song/play/<int:song_id>', methods=['GET', 'POST'])
@login_required
def song(song_id):
    song = Song.query.get_or_404(song_id)
    song_file = url_for('static', filename='uploads/' + song.filename)
    songs = Song.query.order_by(Song.id).all()
    next_song = Song.query.filter(Song.id > song_id).first()
    prev_song = Song.query.filter(
        Song.id < song_id).order_by(Song.id.desc()).first()

    # Query for likes, comments, and replies
    likes = Like.query.filter_by(song_id=song_id).all()
    comments = Comment.query.filter_by(song_id=song_id).all()
    replies = Reply.query.join(Comment, (Reply.comment_id == Comment.id)).filter(
        Comment.song_id == song_id).all()

    # Create forms for likes, comments, and replies
    comment_form = CommentForm()
    reply_form = ReplyForm()

    return render_template('song.html', song=song, music=song_file, songs=songs, next_song=next_song, prev_song=prev_song,
                           likes=likes, comments=comments, replies=replies,
                           comment_form=comment_form, reply_form=reply_form)


@songs.route('/song/edit/<int:song_id>', methods=['GET', 'POST'])
@login_required
def edit(song_id):
    form = SongMetadataForm()
    song = Song.query.get_or_404(song_id)
    if song.owner != current_user and not current_user.is_admin and not current_user.is_manager:
        abort(403)

    if form.validate_on_submit():
        title = form.title.data if form.title.data else "Unknown Title"
        artist_name = form.artist.data if form.artist.data else "Unknown Artist"
        album = form.album.data if form.album.data else "Unknown Album"

        artist_info = Artist_info.query.filter_by(name=artist_name).first()

        # If the artist doesn't exist, create a new Artist_info
        if artist_info is None:
            artist_info = Artist_info(name=artist_name)
            db.session.add(artist_info)
            db.session.commit()

        song.title = title
        song.artist = artist_name
        song.artist_id = artist_info.id  # set the artist_id to the id of the artist_info
        song.album = album
        db.session.commit()

        song_path = os.path.join(
            app.root_path, app.config['UPLOAD_FOLDER'], song.filename)
        audio = eyed3.load(song_path)
        audio.tag.title = title
        audio.tag.artist = artist_name
        audio.tag.album = album
        audio.tag.save()

        flash(f'Song `{title}` has been uploaded!', 'success')
        return redirect(url_for('songs.upload'))
    elif request.method == 'GET':
        form.title.data = song.title
        form.artist.data = song.artist
        form.album.data = song.album
    return render_template('song_metadata.html', title='Edit song details', form=form)


@songs.route('/song/delete/<int:song_id>', methods=['POST'])
@login_required
def delete(song_id):
    song = Song.query.get_or_404(song_id)
    # admin, manager, owner of song can delete it
    if song.owner != current_user and not current_user.is_admin and not current_user.is_manager:
        abort(403)

    song_title = song.title

    # delete the file from the server
    song_path = os.path.join(
        app.root_path, app.config['UPLOAD_FOLDER'], song.filename)
    os.remove(song_path)

    # delete the song from database
    db.session.delete(song)
    db.session.commit()

    flash(f'Song `{song_title}` has been deleted!', 'success')
    return redirect(url_for('main.home'))


@songs.route('/song/download/<int:song_id>', methods=['GET'])
@login_required
def download(song_id):
    song = Song.query.get_or_404(song_id)
    if current_user != song.owner:
        abort(403)

    song_path = os.path.join(app.config['UPLOAD_FOLDER'], song.filename)

    if not os.path.exists(song_path):
        flash("Song file not found on server", "error")
        return redirect(url_for('main.home'))

    title, artist, album = song.title, song.artist, song.album

    response = send_file(song_path, as_attachment=True,
                         download_name=f'{title}.mp3', mimetype='audio/mp3')

    response.headers['Content-Type'] = 'audio/mpeg'
    response.headers['Content-Disposition'] = f'attachment; filename="{title}.mp3"'
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['X-Accel-Redirect'] = f'/download/{song.filename}'

    return response


@songs.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        search_input_text = form.search_input_text.data
        results = Song.query.filter(
            or_(Song.title.ilike('%{}%'.format(search_input_text)),
                Song.artist.ilike('%{}%'.format(search_input_text)),
                Song.album.ilike('%{}%'.format(search_input_text)))).all()

        if results:
            return render_template('search_results.html', songs=results, search_input_text=search_input_text, form=form)
        return render_template('search_results.html', search_input_text=search_input_text, form=form)

    return render_template('search.html', form=form)


@songs.route('/api/search', methods=['POST'])
def search_music_route():
    search_query = request.json.get('query', '')
    results = search_music(search_query)
    return jsonify(results)


@songs.route('/like/<int:song_id>', methods=['POST'])
@login_required
def like(song_id):
    # code to handle liking a song
    song = Song.query.get_or_404(song_id)
    like = Like.query.filter_by(
        user_id=current_user.id, song_id=song_id).first()
    if like:
        db.session.delete(like)
        db.session.commit()
        return jsonify({'liked': False})
    else:
        like = Like(user_id=current_user.id, song_id=song_id)
        db.session.add(like)
        db.session.commit()
        return jsonify({'liked': True})


@songs.route('/comment/<int:song_id>', methods=['POST'])
@login_required
def comment(song_id):
    # code to handle commenting on a song
    song = Song.query.get_or_404(song_id)
    comment = Comment(
        text=request.form['comment'], user_id=current_user.id, song_id=song_id)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('songs.song', song_id=song_id))


@songs.route('/reply/<int:comment_id>', methods=['POST'])
@login_required
def reply(comment_id):
    # code to handle replying to a comment
    comment = Comment.query.get_or_404(comment_id)
    reply = Reply(text=request.form['reply'],
                  user_id=current_user.id, comment_id=comment_id)
    db.session.add(reply)
    db.session.commit()
    return redirect(url_for('songs.song', song_id=comment.song_id))
