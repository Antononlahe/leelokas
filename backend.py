from flask import Flask
from .songbook import create_blueprint
from .database import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
    app.secret_key = 'your_secret_key'
    db.init_app(app)

    songbook_bp = create_blueprint()
    app.register_blueprint(songbook_bp)

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()