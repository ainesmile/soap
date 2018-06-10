from .base import *
import os

DEBUG = False
ALLOWED_HOSTS = ['172.104.107.233']
SECRET_KEY = os.environ.get('SECRET_KEY')