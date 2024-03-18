import unittest
from backend import create_app
from database import db, Song, Author, Genre

class TestDB(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_and_search_song(self):
        # Add a song
        song = Song(name='Test Song', lyrics='Test Lyrics')
        genre = Genre(name='Test Genre')
        author = Author(name='Test Author')
        song.genres.append(genre)
        song.authors.append(author)
        db.session.add(song)
        db.session.commit()

        # Search for the song
        songs = Song.query.filter(Song.name.contains('Test Song')).all()
        self.assertEqual(len(songs), 1)
        self.assertEqual(songs[0].name, 'Test Song')
        self.assertEqual(songs[0].lyrics, 'Test Lyrics')
        self.assertEqual(songs[0].genres[0].name, 'Test Genre')
        self.assertEqual(songs[0].authors[0].name, 'Test Author')

if __name__ == '__main__':
    unittest.main()