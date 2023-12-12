import os
import logging

from .base import *

DEBUG = True
SHELL_PLUS = "ipython"
logger = logging.getLogger(__name__)

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://localhost:5173'
]
