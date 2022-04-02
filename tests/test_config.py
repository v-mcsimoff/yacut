import os

from yacut import app


def test_config():
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///db.sqlite3'
    assert not app.config['SQLALCHEMY_TRACK_MODIFICATIONS']
    assert app.config['SECRET_KEY'] == os.getenv('SECRET_KEY')
