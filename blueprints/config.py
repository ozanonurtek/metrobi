class Config(object):
    API_VERSION = 1.0
    API_TITLE = 'Metrobi API'
    API_DESCRIPTION = 'API that serves metrobi tasks'
    API_CONTACT_EMAIL = 'ozanonurtek@gmail.com'
    API_LICENSE_NAME = 'MIT'
    API_LICENSE_URL = 'https://opensource.org/licenses/MIT'


class DevelopmentConfig(Config):
    # For dev purpose
    pass


class ProductionConfig(Config):
    # For production
    pass


def decide_config(environment):
    try:
        return eval('{}Config'.format(environment))
    except NameError:
        return Config
