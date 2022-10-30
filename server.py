"""Server for Coder's Boost app"""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify, url_for)
from crud import save_encouragement_seen, get_next_encouragement
from model import Encouragement, connect_to_db, db, login_manager
from flask_dance.contrib.github import github
from flask_login import logout_user, login_required, current_user
from  sqlalchemy.sql.expression import func
from oauth import github_blueprint

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
app.register_blueprint(github_blueprint, url_prefix="/login")

app.config["SQLALCHEMY_DATABASE_URI"] ="postgresql:///coders_boost"
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.app = app

db.init_app(app)
login_manager.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/profile")
def user_profile():
    """User profile page that displays personaliazed welcome, language
    preference and favorited encouragements by user."""

@app.route("/github")
def login():
    if not github.authorized:
        return redirect(url_for("github.login"))
    res = github.get("/user")

    return f"You are @{res.json()['login']} on GitHub"

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

#write function to handle if a user is logged in or not.

@app.route("/")
def homepage():
    """Home"""
    #grab a random encouragement
    encouragement = Encouragement.query.order_by(func.random()).first()
    #if the user is logged in, save that they've seen the encouragement
    if current_user.is_authenticated:
        encouragement = get_next_encouragement(current_user)
        save_encouragement_seen(current_user, encouragement)
    
    #call crud function: get_next_encouragement() and 
    #call crud function: save_encouragment_seen()
    return render_template("homepage.html", encouragement=encouragement)



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
    