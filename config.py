import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'mysql+mysqlconnector://root:root@localhost:3306/hotel'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = os.environ.get('ENV') or 'development'
