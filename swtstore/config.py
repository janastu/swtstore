#SECRET_KEY = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
#DATABASE = 'sweets_production'
#DEBUG = True
#ADMIN_USERNAME = 'admin'
#ADMIN_PASSWORD = 'default'
#DB_PORT = 27017
#DB_HOST = 'localhost'
#URL = "http://localhost:5001"

class DefaultConfig():

    """
    Default configuration for Sweet Store application
    """

    DEBUG = True

    SECRET_KEY = '<generate a long, random, unique string and put it here. see\
                 python uuid>'

    SQLALCHEMY_DATABASE_URI =\
        'postgresql+psycopg2://ecthiender:polarbear@localhost/testing'

    SQLALCHEMY_ECHO = True

    #DEFAULT_MAIL_SENDER = 'support@swtr.us'

    DEBUG_LOG = 'logs/debug.log'
    ERROR_LOG = 'logs/error.log'
