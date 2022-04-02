import sys
from pathlib import Path

import pytest
from mixer.backend.flask import mixer as _mixer

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR))


try:
    from yacut import app, db
    from yacut.models import URL_map
except NameError:
    raise AssertionError(
        'Не обнаружен объект приложения. Создайте экземпляр класса Flask и назовите его app.',
    )
except ImportError as exc:
    if any(obj in exc.name for obj in ['models', 'URL_map']):
        raise AssertionError('В файле models не найдена модель URL_map')
    raise AssertionError('Не обнаружен объект класса SQLAlchemy. Создайте его и назовите db.')


@pytest.fixture
def _app(tmp_path):
    db_path = tmp_path / 'test_db.sqlite3'
    db_uri = 'sqlite:///' + str(db_path)
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': db_uri,
        'WTF_CSRF_ENABLED': False,
    })
    with app.app_context():
        db.create_all()
    yield app
    db.drop_all()
    db_path.unlink()


@pytest.fixture
def client(_app):
    return _app.test_client()


@pytest.fixture
def cli_runner():
    return app.test_cli_runner()


@pytest.fixture
def mixer():
    _mixer.init_app(app)
    return _mixer


@pytest.fixture
def short_python_url(mixer):
    return mixer.blend(URL_map, original='https://www.python.org', short='py')
