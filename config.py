"""
The file were the configuration can be defined. The classes can then be used in `app.config.from_object(Config)` in main.py
"""

class Config(object):
    """
    The base class for configurations
    """
    DEBUG = True
    SECRET_KEY = 'super_secret_key'


class ConfigProd(Config):
    """
    This class inherents the Config class and can be used in production.
    """
    DEBUG = False
