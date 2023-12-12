import os
import logging

from .base import *

DEBUG = True
SHELL_PLUS = "ipython"
logger = logging.getLogger(__name__)
ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = [
    'http://acpapp-cluster-alb-936770830.ap-south-1.elb.amazonaws.com',
    'https://v2api.aceonline.app',
    'https://v2.aceonline.app'
]
