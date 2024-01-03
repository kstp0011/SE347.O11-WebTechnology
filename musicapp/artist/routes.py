from flask import render_template, request, Blueprint
from flask_login import current_user, login_required
from musicapp.models import Song, Artist_info
from musicapp.songs.forms import SearchForm

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
def artist_songs(artist_id):
    artist = Artist_info.query.get_or_404(artist_id)
    artist_songs = Song.query.filter_by(artist_id=artist_id).all()
    return render_template('artist_info.html', title=artist.name, artist=artist, artist_songs=artist_songs)