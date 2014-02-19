
class DefaultConfig():

    """
    Default configuration for Sweet Store application
    Copy this sample_config.py file to config.py and edit the values to your
    requirements
    """

    # You can turn debug to False in production
    DEBUG = True # False

    # Secret key needed by the Flask application to create sessions
    SECRET_KEY = '<generate a long, random, unique string and put it here. see\
                 python uuid>'

    # the sqlalchemy database URI
    SQLALCHEMY_DATABASE_URI =\
            'dialect+driver://username:password@host:port/database'

    # sqlalchemy debug messages; turn to False in prdocution
    SQLALCHEMY_ECHO = True #False

    #DEFAULT_MAIL_SENDER = 'support@swtr.us'

    # Configure your log paths
    DEBUG_LOG = 'logs/debug.log'
    ERROR_LOG = 'logs/error.log'
