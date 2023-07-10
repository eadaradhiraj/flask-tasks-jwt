import os

class BaseConfig(object):
	SECRET_KEY = 'o\xadlT\x97\x82\x1e[\xc6aeFv\x90\xdc\xcc'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(BaseConfig):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class DevelopmentConfig(BaseConfig):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'

class ProductionConfig(BaseConfig):
	DEBUG = False