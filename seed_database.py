from itertools import tee
import os
import json
from random import choice, randint
from datetime import datetime
from re import T

from model import db, connect_to_db, User, Encouragement, UserEncouragement


os.system("dropdb coders_boost")
os.system("createdb coders_boost")

def seed_database():
    from server import app
    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.
    connect_to_db(app)
    with db.app.app_context():
      db.create_all()
      u = User(email="jenna.otten@gmail.com")
      db.session.add()
      db.session.commit()


      encouragements = [Encouragement(text="There is a little kid out there that is so glad they'll have you to look up to!"), 
      Encouragement(text="Don't forget why you started!"),
      Encouragement(text="Someday kids like you used to be will look up to you."),
      Encouragement(text="You're making the people who support you so proud."),
      Encouragement(text="Not many people know how hard what you're doing is, but we see you."),
      Encouragement(text="You will be a powerful mentor one day because you understand how hard this road is."),
      Encouragement(text="Your struggle will be worth it. You'll look back on this day and smile"),
      Encouragement(text="You belong in tech. Push your elbows out and make some room for your seat at the table."),
      Encouragement(text="You have learned an unreasonable amount in an impressive amount of time. "),
      Encouragement(text="Keep up the hard work. One day your code could change someone's life.")]
      db.session.add_all(encouragements)
      db.session.commit()
