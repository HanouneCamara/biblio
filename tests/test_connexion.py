from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

try:
    with app.app_context():
        result = db.session.execute(text("SELECT 1"))
        print("Connexion réussie à la base PostgreSQL !")
except Exception as e:
    print("Erreur de connexion :", e)
