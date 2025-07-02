from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from app import db  


#Modèle Utilisateur
class Utilisateur(UserMixin, db.Model):
    __tablename__ = 'utilisateurs'
    
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    
    def __repr__(self) -> str:
        return f"<Utilisateur {self.username}>"