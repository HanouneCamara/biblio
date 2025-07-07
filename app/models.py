from datetime import date
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, DateTime
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
    
#Modèle emprunt
class Emprunt(db.Model):
    __tablename__ = 'emprunts'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom_emprunteur: Mapped[str] = mapped_column(String(100), nullable=False)
    identifiant_emprunteur: Mapped[str] = mapped_column(String(50), nullable=False)
    telephone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)

    livre_id: Mapped[int] = mapped_column(ForeignKey("livres.id"), nullable=False)
    date_emprunt: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    date_retour_prevue: Mapped[date] = mapped_column(Date, nullable=False)
    rendu: Mapped[bool] = mapped_column(Boolean, default=False)

    livre = relationship("Livre", backref="emprunts")

    def __repr__(self):
        return f"<Emprunt {self.nom_emprunteur} - Livre ID {self.livre_id}>"