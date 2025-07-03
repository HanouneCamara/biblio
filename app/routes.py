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

