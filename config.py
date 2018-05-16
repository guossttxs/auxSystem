import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MONGODB_SETTINGS = {
        'db': os.environ.get('MONGO_DB_NAME'),
        'host': os.environ.get('MONGO_DB_HOST'),
        'port': os.environ.get('MONGO_DB_PORT'),
        'username': os.environ.get('MONGO_DB_USERNAME'),
        'password': os.environ.get('MONGO_DB_PWD')
    }
    MONGO_URL = 'mongodb://{}:{}@{}:{}/{}'.format(MONGODB_SETTINGS['username'], MONGODB_SETTINGS['password'],
                                                  MONGODB_SETTINGS['host'], MONGODB_SETTINGS['port'], MONGODB_SETTINGS['db'])

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}