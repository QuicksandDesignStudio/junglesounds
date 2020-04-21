import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    #will change in production
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysuperecretkey')
    JWT_SECRET_KEY =  os.getenv('JWT_SECRET_KEY', 'mysuperecretkey')
    JWT_TOKEN_LOCATION =  ('headers', 'cookies','query_string')
    JWT_ACCESS_TOKEN_EXPIRES = 86400 #one day in seconds
    JWT_QUERY_STRING_NAME = "jwt_token"
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    DB_DIR = os.path.join(basedir, "../../data")
    SAMPLE_AUDIO_UPLOAD_FOLDER = os.path.join(basedir, "../../data/sample_audio")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DB_DIR, 'dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DB_DIR = os.path.join(basedir, "../../data")
    SAMPLE_AUDIO_UPLOAD_FOLDER = os.path.join(basedir, "../../data/sample_audio")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DB_DIR, 'test.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    DB_DIR = "/home/ubuntu/production_data"
    SAMPLE_AUDIO_UPLOAD_FOLDER = os.path.join(DB_DIR, "/sample_audio")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DB_DIR, 'production.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
