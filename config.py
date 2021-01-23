#!/usr/bin/python3
# Author:   @AgbaD | @Agba_dr3

import os

basedir = os.path.abspath(os.path.dirname(__file__))
# password = os.environ.get('DB_PASSWORD')


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "15zn35&m|j91jqo?91[yke34%@2!jyr|8y5?3&hfo$&/sk]"
    WTF_CSRF_SECRET_KEY = os.environ.get("WTF_CSRF_SECRET_KEY") or "35&m|j91jqo?91[yke34%@2!jyr|8y5?3&"
    # ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or "x@x.com"
    # ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or "|j91jqo?91[y"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, "Handbooks") 
    # MAIL_PREFIX = 'The X'

    SSL_DISABLE = True

    @staticmethod
    def init_app(app):
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)


class Development(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    DEBUG = True


class Testing(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    TESTING = True


class Production(Config):
    # username = os.environ.get('DB_USERNAME')
    # db_name = os.environ.get("DB_NAME")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')


class Heroku(Production):
    @classmethod
    def init_app(cls, app):
        Production.init_app(app)
        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

        SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

config = {
    'development': Development,
    'testing': Testing,
    'production': Production,
    'default': Development,
    'heroku': Heroku
}


"""
'postgresql://damilare:{}@localhost:5432/x'.format(
                                  password
                              )
"""