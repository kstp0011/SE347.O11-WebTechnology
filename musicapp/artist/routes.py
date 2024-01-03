from flask import render_template, request, Blueprint, url_for
from flask_login import current_user, login_required
from musicapp.models import Song, Artist_info, Like
from musicapp.songs.forms import SearchForm
from musicapp import db

artists = Blueprint('artists', __name__)


@artists.context_processor
def layout():
    form = SearchForm()
    return dict(form=form)



@artists.route('/artist')
@login_required
def artist():
    page = request.args.get('page', 1, type=int)
    artists = Artist_info.query.paginate(page=page, per_page=12)
    return render_template('artist.html', title='All Artists', artists=artists)


@artists.route('/artist/<int:artist_id>')
@login_required
def artist_info(artist_id):
    artist = Artist_info.query.get_or_404(artist_id)
    artist_songs = Song.query.filter_by(artist_id=artist_id).all()
    if artist.image:
        artist_image = url_for('static', filename='artist_images/' + artist.image)
    else:
        artist_image = url_for('static', filename='artist_images/default.png')
    num_songs = len(artist_songs)
    total_likes = 0
    # for song in artist_songs:
    #     likes_song = Like.query.filter_by(song_id=song.id).all()
    #     likes += len(likes_song)
    return render_template('artist_info.html', title=artist.name, artist=artist, artist_songs=artist_songs, artist_image=artist_image, num_songs=num_songs, total_likes=total_likes, current_user=current_user)