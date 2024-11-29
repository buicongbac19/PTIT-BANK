import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')

class Config:
    SECRET_KEY = "your_secret_key"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(INSTANCE_DIR, 'ptit_database.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False