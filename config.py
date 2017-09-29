class Config(object):
    """
    Common configuration
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    """
    Develompent config
    """
    DEBUG = True
    SQLALCHEMY_ECHO = True
    EXPLAIN_TEMPLATE_LOADING = True


class ProdConfig(Config):
    """
    Production configuration
    """
    DEBUG = False


class TestConfig(Config):
    """
    Testing configuration
    """
    TESTING = True


app_config = {
    'development': DevConfig,
    'production': ProdConfig,
    'testing': TestConfig
}