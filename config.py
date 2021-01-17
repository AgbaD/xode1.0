#!/usr/bin/python3
# Author:   @AgbaD | @Agba_dr3

import os

basedir = os.path.abspath(os.path.dirname(__file__))
password = os.environ.get('DB_PASSWORD')


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "15zn35&m|j91jqo?91[yke34%@2!jyr|8y5?3&hfo$&/sk]"
    # ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or "x@x.com"
    # ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or "|j91jqo?91[y"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # MAIL_PREFIX = 'The NBC'

    @staticmethod
    def init_app(app):
        pass


class Development(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or \
                              'postgresql://damilare:{}@localhost:5432/x'.format(
                                  password
                              )
    DEBUG = True


class Testing(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or \
                              'postgresql://damilare:{}@localhost:5432/x'.format(
                                  password
                              )
    TESTING = True


class Production(Config):
    username = os.environ.get('DB_USERNAME')
    db_name = os.environ.get("DB_NAME")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or \
                             'postgresql://{}:{}@localhost:5432/{}'.format(
                                  username, password, db_name
                              )


config = {
    'development': Development,
    'testing': Testing,
    'production': Production,
    'default': Development
}
