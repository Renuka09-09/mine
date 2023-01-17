import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY=os.environ.grt('SECRET_KEY') or 'test-key-motherfucker'
    SQLALCHEMY_DARTABASE-URI='mysql://root@127.0.0.1:3360/alchemy'
    SQLALCHEMY_TRACT_MODIFICATIONS=False
