"""Server for Coder's Boost app"""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify, url_for)
from crud import save_encouragement_seen, get_next_encouragement, save_user_encouragement
from model import Encouragement, connect_to_db, db, login_manager, UserEncouragement
from flask_dance.contrib.github import github
from flask_login import logout_user, login_required, current_user
from sqlalchemy.sql.expression import func
from oauth import github_blueprint
from flask_babel import Babel

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
app.register_blueprint(github_blueprint, url_prefix="/login")
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'

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
        #if not logged in flash message that user must be logged in 
        flash("Please log in with github to view your profile page.")  #try to fis this flash message...it's not showing up. (look this up)
        return redirect(url_for("homepage"))
    
    return render_template("profile.html", user_encouragements=user_encouragements)

@app.route("/delete-favorite", methods=["POST"])
def delete_favorite():
    """Deletes a favorited encouragement from a user's profile page."""

    #had to get the json body from the post request because before, it was trying to convert None to an integer
    content = request.json
    #get a specific encouragement on a user's profile, using the user_id and the encouragement_id
    encouragement_id = int(content.get("encouragement_id"))
    #getting one user favorited encouragement, take in the logged in user (current_user_id) so some user can't delete another user's encouragement
    user_encouragement = UserEncouragement.query.filter(UserEncouragement.user_id==current_user.id, UserEncouragement.encouragement_id==encouragement_id).one()
    #reset favorited_at timestamp to None (to "delete") favorited encouragement
    user_encouragement.favorited_at = None
    db.session.add(user_encouragement)
    db.session.commit()

    return ""

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

@app.route("/", methods=("GET", "POST"))
def homepage():
    """View function for homepage."""
    #grab a random encouragement, if they've hit the button
    encouragement = None
    if request.method == "POST": #when form is submitted (button) to get a boost
        if current_user.is_authenticated:
            #if the user is logged in, save that they've seen the encouragement
            encouragement = get_next_encouragement(current_user)
            save_encouragement_seen(current_user, encouragement)
        else:
            encouragement = Encouragement.query.order_by(func.random()).first()
    
    encouragement_id = request.args.get('encouragement_id') #get a specific encouragement from the query string parameter
                                      #convert to integer because it's returned as a string
    if encouragement_id: #check if encouragement_id in url (if enc_id is not = None)
        encouragement_id = int(encouragement_id)
        #FIX: handles for if id is not an integer (edgecase)
        #if encouragement_id:
        encouragement = Encouragement.query.filter_by(id=encouragement_id).first() #get a specific encouragement, filtering by id

        #else: 
            #return redirect(url_for("homepage"))

    return render_template("homepage.html", encouragement=encouragement)

# https://stackoverflow.com/questions/34558264/fetch-api-with-cookie

@app.route("/resources")
def resources():
    """View function for resources page."""

    return render_template("resources.html")

@babel.localeselector
def get_locale():
   
    return 'es'

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
    