import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLE = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change_me')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(basedir, 'app.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def __init__(self):
        print('Using {} ...'.format(self.__class__.__name__))


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


TEST_DB = 'test_pledg_lite.db'
TEST_DB_PATH = "/opt/project/data/{}".format(TEST_DB)


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + TEST_DB_PATH
