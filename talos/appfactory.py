from flask import Flask
from .middleware import activate_middleware


class DevelopmentConfig(object):
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = '857de896a3ad275824157a245a057f5c'
    FLASK_SECRET = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = 'True'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


class ProductionConfig(DevelopmentConfig):
    DEVELOPMENT = False
    DEBUG = False


def make_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    activate_middleware(app)
    return app