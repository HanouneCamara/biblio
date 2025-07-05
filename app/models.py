from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, Integer, String, DateTime
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
    
#Modèle Livre
class Livre(db.Model):
    __tablename__ = 'livres'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    titre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    auteur: Mapped[str] = mapped_column(String(100), nullable=False)
    annee: Mapped[int] = mapped_column(Integer, default=2000, nullable=False)
    nombre_exemplaires: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    disponible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    date_ajout: Mapped[DateTime] = mapped_column(DateTime, nullable=False, server_default=db.func.now())
    
    def __repr__(self):
        return f"<Livre {self.titre} par {self.auteur}>"