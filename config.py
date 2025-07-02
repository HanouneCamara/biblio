import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://biblio_admin:biblio@localhost/biblio_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)