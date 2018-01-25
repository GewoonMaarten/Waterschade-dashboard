class Config(object):
    DEBUG = True
    SECRET_KEY = 'super_secret_key'


class ConfigProd(Config):
    DEBUG = False
