"""Server for Coder's Boost app"""

import click
from flask.cli import with_appcontext
from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from flask_babel import Babel
from flask_dance.contrib.github import github
from flask_login import current_user, login_required, logout_user
from jinja2 import StrictUndefined
import os
from sqlalchemy.sql.expression import func

from crud import (get_next_encouragement, save_encouragement_seen,
                  save_user_encouragement, delete_user_favorite)
from model import Encouragement, UserEncouragement, db, login_manager, User
from oauth import github_blueprint
from onesignal import send_email
from dotenv import load_dotenv
load_dotenv()
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
app.register_blueprint(github_blueprint, url_prefix="/login")
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'

db_uri = os.getenv("DATABASE_URL")
if db_uri.startswith("postgres://"):
    db_uri = db_uri.replace("postgres://","postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
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
        #if not logged in redirect to homepage
        redirect(url_for("homepage"))
    
    return render_template("profile.html", user_encouragements=user_encouragements)

@app.route("/delete-favorite", methods=["POST"])
def delete_favorite():
    """Deletes a favorited encouragement from a user's profile page."""

    #had to get the json body from the post request because before, it was trying to convert None to an integer
    content = request.json
    #get a specific encouragement on a user's profile, using the user_id and the encouragement_id
    encouragement_id = int(content.get("encouragement_id"))
    #call crud function that saves this change to the data base
    delete_user_favorite(current_user.id, encouragement_id)
 
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
    #grab an encouragement, if they've hit the button
    encouragement = None
    if request.method == "POST": #when form is submitted (button) to get a boost
        if current_user.is_authenticated: #is_authenticated is part of flask login (see flask docs)
            #if the user is logged in, save that they've seen the encouragement
            encouragement = get_next_encouragement(current_user, get_locale()) #get the language with get_locale()
            save_encouragement_seen(current_user, encouragement)
        else:
             #get random encouragement filtered by language (with get_locale()) and return one random pick from db
            encouragement = Encouragement.query.filter_by(language=get_locale()).order_by(func.random()).first()
       
        
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
   
    if "language" in session: #check if language (en or es) is in session
        return session['language'] # if so, return session language user chose
    
    return request.accept_languages.best_match(['en', 'es']) #if they don't have language set, return what browser is set to

@app.route("/language/<language>") #will use this <language> variable to populate if es or eng is chosen, so you don't have to use a form
def language(language):
    """Changes site from English to Spanish"""

    if language in {'en', 'es'}:
        session['language'] = language

    return ""

@app.route("/profile/email", methods=["POST"])
def update_email():
    
    #data being sent from user's browser in json 
    content = request.json
    #get email from json body data
    email = content.get("email")
    #get user object from db
    user = User.query.filter(User.id==current_user.id).one()
    #change user's email to the one they just sent in json body, set to email variable
    user.email = email
    #store user in db
    db.session.add(user)
    db.session.commit()

    return ""

@click.command(name='send-daily-email') #creating a custom command in flask, see geeksforgeeks for syntax & instructions
@with_appcontext
def send_daily_email():
    #get an encouragement:
    #get random encouragement filtered by language (with get_locale()) and return one random pick from db
    encouragement = Encouragement.query.filter_by(language="").order_by(func.random()).first()
    #get all users with an email address
    users = User.query.filter(User.email != None).all()
    #iterate through all users
    for user in users:
    #send them a daily encouragement in an email, using function from onesignal.py
        send_email(user.email, encouragement.text)

    return ""

app.cli.add_command(send_daily_email) #registering this command with flask app



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
    