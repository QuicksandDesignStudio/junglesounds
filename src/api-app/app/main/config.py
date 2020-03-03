import os


basedir = os.path.abspath(os.path.dirname(__file__))

dbdir = os.path.join(basedir, "../../data")

print(basedir)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysuperecretkey')
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(dbdir, 'dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(dbdir, 'test.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(dbdir, 'production.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
