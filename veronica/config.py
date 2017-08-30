class DefaultConfig(object):
    DEBUG = False


class DevelopmentConfig(DefaultConfig):
    DEBUG = True


class TestConfig(DefaultConfig):
    PRESERVE_CONTEXT_ON_EXCEPTION = True
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False


config_env_files = {
    'test': 'veronica.config.TestConfig',
    'development': 'veronica.config.DevelopmentConfig'
}
