from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

song_authors = db.Table('song_authors',
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key=True),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'), primary_key=True)
)

song_genres = db.Table('song_genres',
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True)
)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    lyrics = db.Column(db.Text, nullable=False)
    authors = db.relationship('Author', secondary=song_authors, lazy='subquery',
        backref=db.backref('songs', lazy=True))
    genres = db.relationship('Genre', secondary=song_genres, lazy='subquery',
        backref=db.backref('songs', lazy=True))

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
