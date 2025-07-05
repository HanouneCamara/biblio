from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Utilisateur, Livre
from app import db

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
        
        #Afficher livres
        livres = Livre.query.all()
        
        return render_template('index.html', livres=livres)

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
            annee = request.form.get("annee")
            nombre_exemplaires = request.form.get("nombre_exemplaires")
            
            # Vérifier que les champs sont remplis
            if not titre or not auteur or not annee or not nombre_exemplaires:
                flash("Tous les champs sont obligatoires.")
                return render_template("ajouter_livre.html")
            try:
                annee = int(annee)
                nombre_exemplaires = int(nombre_exemplaires)
            except ValueError:
                flash("L'année et le nombre d'exemplaires doivent être des nombres entiers.")
                return render_template("ajouter_livre.html")
            
            # Vérifier l’unicité du titre
            if Livre.query.filter_by(titre=titre).first():
                flash("Ce livre existe déjà.")
                return render_template("ajouter_livre.html")
            
            # Créer et enregistrer
            livre = Livre(
                titre=titre,
                auteur=auteur,
                annee=annee,
                nombre_exemplaires=nombre_exemplaires
            )
            
            db.session.add(livre)
            db.session.commit()

            flash("Livre ajouté avec succès.")
            return redirect(url_for("index"))

        return render_template("ajouter_livre.html")

    #Modifier livre
    @app.route('/livres/modifier/<int:livre_id>', methods=['GET', 'POST'])
    def modifier(livre_id):
        livre = Livre.query.get_or_404(livre_id)
        if request.method == 'POST':
            titre = request.form.get('titre')
            auteur = request.form.get('auteur')
            annee = request.form.get('annee')
            nombre_exemplaires = request.form.get('nombre_exemplaires')
            disponible = request.form.get('disponible') == 'on'
            
            if not titre or not auteur or not annee or not nombre_exemplaires:
                flash("Tous les champs sont obligatoires.")
                return render_template('modifier_livre.html', livre=livre)
            
            try:
                annee = int(annee)
                nombre_exemplaires = int(nombre_exemplaires)
            except ValueError:
                flash("L'année et le nombre d'exemplaires doivent être des nombres entiers.")
                return render_template('modifier_livre.html', livre=livre)
            
            # Vérifier unicité du titre sauf pour ce livre
            livre_exist = Livre.query.filter(Livre.titre == titre, Livre.id != livre.id).first()
            if livre_exist:
                flash("Un autre livre avec ce titre existe déjà.")
                return render_template('modifier_livre.html', livre=livre)

            livre.titre = titre
            livre.auteur = auteur
            livre.annee = annee
            livre.nombre_exemplaires = nombre_exemplaires
            livre.disponible = disponible

            db.session.commit()
            flash("Livre modifié avec succès.")
            return redirect(url_for('index'))
        
        return render_template('modifier_livre.html', livre=livre)
    
    #Supprimer livre
    @app.route('/livres/supprimer/<int:livre_id>', methods=['POST', 'GET'])
    @login_required
    def supprimer(livre_id):
        livre = Livre.query.get_or_404(livre_id)
        if request.method == 'POST':
            db.session.delete(livre)
            db.session.commit()
            flash("Livre supprimé avec succès.")
            return redirect(url_for('index'))
        # Si GET, afficher confirmation simple
        return render_template('confirmer_suppression.html', livre=livre)