from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Utilisateur

def register_routes(app):
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            utilisateur = Utilisateur.query.filter_by(username=username).first()

            if utilisateur and utilisateur.check_password(password):
                login_user(utilisateur)
                return redirect(url_for("index"))
            else:
                flash("Nom d’utilisateur ou mot de passe incorrect")

        return render_template("login.html")

    @app.route('/')
    @login_required
    def index():
        return render_template('index.html')

    # Nouvelle route pour rediriger /index vers /
    @app.route('/index')
    @login_required
    def index_redirect():
        return redirect(url_for('index'))

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))
    
    #route livre
    @app.route("/livres/ajouter", methods=["GET", "POST"])
    @login_required
    def ajouter():
        if request.method == "POST":
            titre = request.form.get("titre")
            auteur = request.form.get("auteur")
            
            # Vérifier que les champs sont remplis
            if not titre or not auteur:
                flash("Tous les champs sont obligatoires.")
                return render_template("ajouter_livre.html")
            
            # Vérifier l’unicité du titre
            from app.models import Livre
            if Livre.query.filter_by(titre=titre).first():
                flash("Ce livre existe déjà.")
                return render_template("ajouter_livre.html")
            
            # Créer et enregistrer
            livre = Livre(titre=titre, auteur=auteur)
            from app import db
            db.session.add(livre)
            db.session.commit()

            flash("Livre ajouté avec succès.")
            return redirect(url_for("index"))

        return render_template("ajouter_livre.html")
