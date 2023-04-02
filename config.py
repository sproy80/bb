# https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/#install-requirements
# Refer to above URL to setup database
# Credentials : postgres - admin123
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_DATABASE_URI = "postgresql:///trade_analysis"

# $ export DATABASE_URL="postgresql:///wordcount_dev"
# To setup environment varriable


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
