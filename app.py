"""Server for Coder's Boost app"""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify, url_for)
from crud import save_encouragement_seen, get_next_encouragement, save_user_encouragement
from model import Encouragement, connect_to_db, db, login_manager, UserEncouragement
from flask_dance.contrib.github import github
from flask_login import logout_user, login_required, current_user
from sqlalchemy.sql.expression import func
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
def profile():
    """View function for user profile page that displays personaliazed welcome, language
    preference and favorited encouragements by user."""
    if current_user.is_authenticated:
     #show favorited encouragements by user
        user_encouragements = UserEncouragement.query.filter(UserEncouragement.user_id==current_user.id, UserEncouragement.favorited_at != None).all()
    else:
        flash("Please log in with github to view your profile page.")
    #if not logged in flash message that user must be logged in 
    #TODO:

    #make a share button

    return render_template("profile.html", user_encouragements=user_encouragements)

@app.route("/user-encouragement", methods=["POST"]) #hidden route that grabs what I need to save fav_encouragements to profile page
def user_encouragement():
    """Gets user_id and encouragement_id and saves it."""

    user_id = int(request.form.get("user_id"))
    encouragement_id = int(request.form.get("encouragement_id"))
    save_user_encouragement(user_id, encouragement_id)

    return redirect(url_for("homepage"))

@app.route("/github") #Github OAuth route
def login():
    if not github.authorized:
        return redirect(url_for("github.login"))

    return redirect(url_for("homepage"))

@app.route("/logout") #Github OAuth route
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

#write function to handle if a user is logged in or not.

@app.route("/", methods=("GET", "POST"))
def homepage():
    """View function for homepage."""
    #grab a random encouragement, if they've hit the button
    encouragement = None
    if request.method == "POST":
        if current_user.is_authenticated:
            #if the user is logged in, save that they've seen the encouragement
            encouragement = get_next_encouragement(current_user)
            save_encouragement_seen(current_user, encouragement)
        else:
            encouragement = Encouragement.query.order_by(func.random()).first()

    #handle for if user is not logged in and tries to favorite an encouragement
    
    return render_template("homepage.html", encouragement=encouragement)

@app.route("/resources")
def resources():
    """View function for resources page."""

    return render_template("resources.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
    