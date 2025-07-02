from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from app import db
from werkzeug.security import generate_password_hash, check_password_hash



#Modèle Utilisateur
class Utilisateur(UserMixin, db.Model):
    __tablename__ = 'utilisateurs'
    
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    
    def __repr__(self) -> str:
        return f"<Utilisateur {self.username}>"
    
    #Hacher et stocker
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
       
    #vérifier un mot de passe donné
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)