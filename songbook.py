from flask import Blueprint, request, render_template, session, redirect, url_for, make_response, jsonify
from .database import db, Song, Author, Genre

def create_blueprint():
    bp = Blueprint('songbook', __name__)

    @bp.route('/', methods=['GET'])
    def root():
        return redirect(url_for('songbook.index'))

    @bp.route('/songbook', methods=['GET'])
    def index():
        query = request.args.get('query', '')
        search_in_lyrics = 'search_in_lyrics' in request.args
        session['search_in_lyrics'] = search_in_lyrics
        sort = session.get('sort', 'name')
        if 'flip_sort' in request.args:
            sort = 'lyrics' if sort == 'name' else 'name'
            session['sort'] = sort
            redirect_args = {'query': query}
            if search_in_lyrics:
                redirect_args['search_in_lyrics'] = 'on'
            return redirect(url_for('songbook.index', **redirect_args))
        # QUERY
        if query == '':
            songs = Song.query.all()
        else:
            song = Song.query.filter_by(name=query).first()
            if song is not None:
                return redirect(url_for('songbook.show_song', song_name=song.name))
            if search_in_lyrics:
                songs = Song.query.filter(Song.name.contains(query) | Song.lyrics.contains(query)).all()
            else:
                songs = Song.query.filter(Song.name.contains(query)).all()
        for song in songs:
            song.lyrics = song.lyrics.replace('Refr.', '').replace(':,:', '').strip()
        # SORT
        if sort == 'lyrics':
            songs.sort(key=lambda song: song.lyrics.split(' ')[0].lower())
        else:
            songs.sort(key=lambda song: song.name.lower())
        songs_dict = [song.to_dict() for song in songs]
        return render_template('index.html', songs=songs_dict)

    @bp.route('/songbook/add', methods=['POST'])
    def add_song():
        song_id = request.form.get('song_id')
        name = request.form.get('name').strip()
        lyrics = request.form.get('lyrics').strip()
        genre_names = request.form.get('genre').strip().split(',')
        author_names = request.form.get('author').strip().split(',')

        if song_id:
            song = Song.query.get(song_id)
            if song is None:
                return "Song not found", 404
            song.name = name
            song.lyrics = lyrics
            song.genres.clear()
            song.authors.clear()
        else:
            song = Song(name=name, lyrics=lyrics)
            db.session.add(song)

        for genre_name in genre_names:
            genre_name = genre_name.strip()
            if genre_name:
                genre = Genre.query.filter_by(name=genre_name).first()
                if genre is None:
                    genre = Genre(name=genre_name)
                    db.session.add(genre)
                if genre not in song.genres:
                    song.genres.append(genre)

        for author_name in author_names:
            author_name = author_name.strip()
            if author_name:
                author = Author.query.filter_by(name=author_name).first()
                if author is None:
                    author = Author(name=author_name)
                    db.session.add(author)
                if author not in song.authors:
                    song.authors.append(author)

        db.session.add(song)
        db.session.commit()

        response_content = """
            Song successfully added.<br>
            <button onclick="location.href='/songbook/admin';">Back to Admin</button>
        """
        return make_response(response_content, 201)
    
    @bp.route('/songbook/<string:song_name>', methods=['GET'])
    def show_song(song_name):
        song = Song.query.filter_by(name=song_name).first_or_404()
        return render_template('song.html', song=song)

    @bp.route('/songbook/song/<int:song_id>', methods=['GET'])
    def get_song(song_id):
        song = Song.query.get(song_id)
        if song is None:
            return jsonify({'error': 'Song not found'}), 404
        return jsonify({
            'name': song.name,
            'lyrics': song.lyrics,
            'genre': ', '.join(genre.name for genre in song.genres),
            'author': ', '.join(author.name for author in song.authors),
        })

    @bp.route('/songbook/delete', methods=['GET', 'POST'])
    def delete_song():
        if request.method == 'POST':
            song_id = request.form.get('song_id')
            song = Song.query.get(song_id)
            if song:
                db.session.delete(song)
                db.session.commit()
                return "Song deleted", 200
            else:
                return "Song not found", 404
        else:
            songs = Song.query.all()
            return render_template('delete.html', songs=songs)
        
    @bp.route('/songbook/admin', methods=['GET', 'POST'])
    def admin():
        auth = request.authorization
        if not auth or auth.password != 'pw1':
            return make_response(
                'Could not verify your access level for that URL.\n'
                'You have to login with proper credentials', 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'})
        else:
            if request.method == 'POST':
                song_id = request.form.get('song_id')
                song = Song.query.get(song_id)
                if song:
                    db.session.delete(song)
                    db.session.commit()
                    return "Laul kustutatud", 200
                else:
                    return "Song not found", 404
            else:    
                songs = Song.query.all()
                return render_template('admin.html', songs=songs)

    return bp