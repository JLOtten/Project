"""Server for Coder's Boost app"""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

from model import Encouragement, db, connect_to_db

@app.route("/")
def homepage():
    """Home"""

    encouragement = Encouragement.query.filter().first()
    return render_template("homepage.html", encouragement=encouragement)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
    