from flask import Blueprint, request, render_template, abort, redirect, url_for
from .database import db, Song, Author, Genre

def create_blueprint():
    bp = Blueprint('songbook', __name__)

    @bp.route('/songbook', methods=['GET'])
    def index():
        query = request.args.get('query', '')
        sort = request.args.get('sort', '')
        if query == '':
            songs = Song.query.all()
        else:
            song = Song.query.filter_by(name=query).first()
            if song is not None:
                return redirect(url_for('songbook.song_detail', song_name=song.name))
            songs = Song.query.filter(Song.name.contains(query) | Song.lyrics.contains(query)).all()
        if sort == 'alphabet':
            songs.sort(key=lambda song: song.name)
        elif sort == 'lyrics':
            songs.sort(key=lambda song: song.lyrics.split(' ')[0])
        song_names = [song.name for song in songs]

        for song in songs:
            song.first_three_words = ' '.join(song.lyrics.split(' ')[:3])
        return render_template('index.html', songs=songs, song_names=song_names)   

    @bp.route('/songbook/add', methods=['GET', 'POST'])
    def add_song():
        if request.method == 'POST':
            name = request.form.get('name').strip()
            lyrics = request.form.get('lyrics').strip()
            genre_names = request.form.get('genre').strip().split(',')
            author_names = request.form.get('author').strip().split(',')

            song = Song(name=name, lyrics=lyrics)

            for genre_name in genre_names:
                genre = Genre.query.filter_by(name=genre_name.strip()).first()
                if genre is None:
                    genre = Genre(name=genre_name.strip())
                    db.session.add(genre)
                song.genres.append(genre)

            for author_name in author_names:
                author = Author.query.filter_by(name=author_name.strip()).first()
                if author is None:
                    author = Author(name=author_name.strip())
                    db.session.add(author)
                song.authors.append(author)

            db.session.add(song)
            db.session.commit()

            return render_template('song_added.html')
        else:
            return render_template('add_song.html')


    @bp.route('/songbook/search', methods=['GET'])
    def search_songs():
        query = request.args.get('query', '')

        if query == '':
            songs = Song.query.all()
        else:
            songs = Song.query.filter(Song.name.contains(query) | Song.lyrics.contains(query)).all()
            songs.extend(Author.query.filter(Author.name.contains(query)).all())
            songs.extend(Genre.query.filter(Genre.name.contains(query)).all())

        return {'songs': [song.name for song in songs]}
    
    @bp.route('/songbook/<int:song_id>', methods=['GET'])
    def show_song_by_id(song_id):
        song = Song.query.get(song_id)
        return render_template('song.html', song=song)

    @bp.route('/songbook/<int:song_id>', methods=['GET'])
    def song_detail_by_id(song_id):
        song = Song.query.get(song_id)
        if song is None:
            abort(404, description="No song found with the given ID.")
        return render_template('song_detail.html', song=song)
    
    @bp.route('/songbook/<string:song_name>', methods=['GET'])
    def show_song(song_name):
        song = Song.query.filter_by(name=song_name).first_or_404()
        return render_template('song.html', song=song)

    @bp.route('/songbook/<string:song_name>', methods=['GET'])
    def song_detail(song_name):
        song = Song.query.filter_by(name=song_name).first_or_404()
        return render_template('song_detail.html', song=song)

    @bp.route('/songbook/delete', methods=['GET', 'POST'])
    def delete_song():
        if request.method == 'POST':
            password = request.form.get('password')
            song_id = request.form.get('song_id')
            if password == 'hardcoded_password':
                song = Song.query.get(song_id)
                if song:
                    db.session.delete(song)
                    db.session.commit()
                    return redirect(url_for('index'))
                else:
                    return "Song not found", 404
            else:
                return "Invalid password", 403
        else:
            songs = Song.query.all()
            return render_template('delete.html', songs=songs)

    return bp