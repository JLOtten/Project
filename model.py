"""Models for Coders' Boost app"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """A User"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True,)
    email = db.Column(db.String, unique = True,)
    username = db.Column(db.String)

    encouragements = db.relationship("UserEncouragement", back_populates= "user")

    def __repr__(self):
        """Show user info"""

        return f'<User user_id={self.id} email={self.email}'

class Encouragement(db.Model):
    """Stored compliment and meta data"""

    __tablename__ = "encouragements"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True,)
    text = db.Column(db.String, unique = True,)
    language = db.Column(db.String,)
    created_at = db.Column(db.DateTime,)
    
    user_encouragements = db.relationship("UserEncouragement", back_populates = "encouragement")

class UserEncouragement(db.Model):
    """A middle table to connect Users and Compliments"""

    __tablename__ = "user_encouragements"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    encouragement_id = db.Column(db.Integer, db.ForeignKey("encouragements.id"),)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"),)
    created_at = db.Column(db.DateTime,)
    favorited_at = db.Column(db.DateTime, nullable=True)
    last_viewed_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship("User", back_populates = "encouragements")
    encouragement = db.relationship("Encouragement", back_populates = "user_encouragements")

class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

def connect_to_db(flask_app, db_uri="postgresql:///coders_boost", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from app import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)