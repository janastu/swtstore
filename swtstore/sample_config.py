

class DefaultConfig():

    """
    Default configuration for Sweet Store application
    Copy this sample_config.py file to config.py and edit the values to your
    requirements
    """

    # You can turn debug to False in production
    DEBUG = True  # False

    # Secret key needed by the Flask application to create sessions
    SECRET_KEY = '<generate a long, random, unique string and put it here. see\
                 python uuid>'

    # the sqlalchemy database URI
    # postgresql+psycopg2://user:password@localhost:5432/test
    # Creation of ``user`` user with access to ``test`` database should have
    # been done prior to editing this line.
    # Refer https://wiki.debian.org/PostgreSql#User_access for creating users
    # in postgresql.
    SQLALCHEMY_DATABASE_URI = 'dialect+driver://username:password@host:port/database'

    # Log level for the application
    LOG_LEVEL = 'ERROR'

    # sqlalchemy debug messages; turn to False in prdocution
    SQLALCHEMY_ECHO = True  # False

    # DEFAULT_MAIL_SENDER = 'support@swtr.us'

    # Configure your log paths
    LOG_FILE = 'logs/swtstore.log'

    # The Mozilla Persona Verifier Host. Leave it as it is.
    MOZ_PERSONA_VERIFIER = 'https://verifier.login.persona.org/verify'

    # The URL at which this app, swtstore, is deployed.
    SWTSTORE_URL = 'http://demo.swtr.us'

    # Bearer token expiry (in seconds)
    OAUTH2_PROVIDER_TOKEN_EXPIRES_IN = 3600
