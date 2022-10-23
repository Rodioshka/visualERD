import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(join(dirname(__file__), '.env'))


DB = {
    'HOST': os.getenv('HOST'),
    'USER': os.getenv('USER'),
    'PASSWORD': os.getenv('PASSWORD'),
    'PORT': os.getenv('PORT'),
    'DB_NAME': os.getenv('DB'),
}