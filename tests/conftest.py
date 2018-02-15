import pytest

from app import app as _app, db as _db


def pytest_configure(config):
    """Set the app to testing mode."""
    import sys
    sys._is_testing = True


def pytest_unconfigure(config):
    """Unset the `_is_testing` var."""
    import sys
    del sys._is_testing


"""Notes: Test settings are based on: http://alexmic.net/flask-sqlalchemy-pytest/"""


@pytest.fixture(scope='session')
def app(request):
    """Session-wide test application."""
    # Establish an application context before running the tests.
    ctx = _app.app_context()  # TODO: Not sure if it is necessary.
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return _app


@pytest.fixture(scope='session')
def db(request):
    """Session-wide test database."""
    def teardown():
        _db.drop_all()

    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    _session = db.create_scoped_session(options=options)

    db.session = _session

    yield _session

    transaction.rollback()
    connection.close()
    _session.remove()
