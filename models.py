#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

from flask_sqlalchemy import SQLAlchemy
from forms import *

db = SQLAlchemy()


class Venue(db.Model):
    # TODO: implement any missing fields, as a database migration using - DONE
    # Flask-Migrate
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    # state = db.Column(db.String(120))
    state = db.Column(db.Enum(StateEnum), nullable=False)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    # genres = db.Column(db.ARRAY(db.String))
    genres = db.Column(db.ARRAY(db.Enum(GenreEnum)), nullable=False)
    shows = db.relationship('Show', backref='venue', lazy=True)


class Artist(db.Model):
    # TODO: implement any missing fields, as a database migration using - DONE
    # Flask-Migrate
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    # state = db.Column(db.String(120))
    state = db.Column(db.Enum(StateEnum), nullable=False)
    phone = db.Column(db.String(120))
    # genres = db.Column(db.ARRAY(db.String))
    genres = db.Column(db.ARRAY(db.Enum(GenreEnum)), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    website = db.Column(db.String(120))

    shows = db.relationship('Show', backref='artist', lazy=True)


class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)

    artist_id = db.Column(
        db.Integer,
        db.ForeignKey('Artist.id'),
        nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)


# TODO Implement Show and Artist models, and complete all model
# relationships and properties, as a database migration. - DONE
