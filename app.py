#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from models import db, Venue, Artist, Show
from datetime import datetime
from forms import *
from hmac import compare_digest as safe_str_cmp
from flask_wtf.csrf import CSRFProtect
from flask_wtf import Form
from logging import Formatter, FileHandler
import os
import logging
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
import babel
import dateutil.parser
import json
import sys
print(sys.path)


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

print("initialise falsk app")
app = Flask(__name__)
app.config.from_object(Config)


print("Initialise extensions")
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
print("Extensions initialised")

# Initialize CSRF protection
csrf = CSRFProtect(app)

# TODO: connect to a local postgresql database - DONE
# this is in the config file?


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    # num_upcoming_shows should be aggregated based on number of upcoming
    # shows per venue. - DONE

    # I think this is the hidden field. I think I added it
    # but I cannot remember
    form = SearchForm()

    # Query db to get all venues
    venues = Venue.query.all()

    # create a set of unique city and state pairs
    cities = set()
    for venue in venues:
        cities.add((venue.city, venue.state))

    # get data by city and state
    data = []
    for city, state in cities:
        city_venues = Venue.query.filter_by(city=city, state=state).all()
        venues_data = []
        for venue in city_venues:
            venues_data.append({
                "id": venue.id,
                "name": venue.name,
            })
        data.append({
            "city": city,
            "state": state,
            "venues": venues_data
        })

    return render_template('pages/venues.html', areas=data, form=form)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on venues with partial string search. Ensure it
    # is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live
    # Music & Coffee" - DONE
    form = SearchForm()
    search_term = request.form.get('search_term', '')
    search = "%{}".format(search_term)
    results = Venue.query.filter(Venue.name.ilike(search)).all()

    data = []
    for venue in results:
        num_upcoming_shows = Show.query.filter(Show.venue_id == venue.id,
                                               Show.start_time > datetime.now()).count()
        data.append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": num_upcoming_shows
        })

    response = {
        "count": len(results),
        "data": data
    }

    return render_template('pages/search_venues.html', results=response,
                           search_term=search_term, form=form)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    # - DONE
    form = SearchForm()
    venue = Venue.query.get(venue_id)

    if not venue:
        return render_template('errors/404.html'), 404

    past_shows = []
    upcoming_shows = []
    current_time = datetime.now()

    for show in venue.shows:
        show_data = {
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        if show.start_time < current_time:
            past_shows.append(show_data)
        else:
            upcoming_shows.append(show_data)

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
    }

    return render_template('pages/show_venue.html', venue=data, form=form)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead - DONE
    form = VenueForm(request.form)
    if form.validate_on_submit():
        try:
            new_venue = Venue(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                address=form.address.data,
                phone=form.phone.data,
                image_link=form.image_link.data,
                facebook_link=form.facebook_link.data,
                website=form.website.data,
                seeking_talent=form.seeking_talent.data,
                seeking_description=form.seeking_description.data,
                genres=form.genres.data
            )
            db.session.add(new_venue)
            db.session.commit()
            # TODO: modify data to be the data object returned from db
            # insertion
            # on successful db insert, flash success
            flash('Venue ' + form.name.data + ' was successfully listed!')

            # return redirect(url_for('index')) - not sure I need to do this

            # TODO: on unsuccessful db insert, flash an error instead. - DONE
            # e.g., flash('An error occurred. Venue ' + data.name + ' could
            # not be listed.')
            # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Venue ' + form.name.data + ' could not \
                  be listed.')
            print(f'Error: {e}')
            return render_template('forms/new_venue.html', form=form)
        finally:
            db.session.close()
    else:
        print("Form errors:", form.errors)
        flash("Venue form validation failed. Please check the errors and try again.")
    return render_template('pages/home.html', form=form)


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using - DONE
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit
    # could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page,
    # have it so that
    # clicking that button delete it from the db then redirect the user to the
    # homepage
    try:
        venue = Venue.query.get(venue_id)
        if not venue:
            return jsonify({"success": False, "message": "Venue not found"}),
            404

        db.session.delete(venue)
        db.session.commit()
        flash("Venue was successfully deleted!")
        return jsonify({"sucess": True}), 200
    except Exception as e:
        db.session.rollback()
        flash("An error occured. Venue could not be deleted")
        print(f'Error: {e}')
        return jsonify({"success": False, "message": "Fail"}), 500
    finally:
        db.session.close()

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database - DONE
    form = SearchForm()
    artists = Artist.query.all()

    data = []
    for artist in artists:
        data.append({
            "id": artist.id,
            "name": artist.name
        })

    return render_template("pages/artists.html", artists=data, form=form)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it
    # is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The
    # Wild Sax Band".
    # search for "band" should return "The Wild Sax Band". - DONE
    form = SearchForm()
    search_term = form.search_term.data.strip()
    search = f"%{search_term}%"  # This adds partial searching.
    results = Artist.query.filter(Artist.name.ilike(search)).all()

    data = []
    for artist in results:
        num_upcoming_shows = Show.query.filter(
            Show.artist_id == artist.id,
            Show.start_time > datetime.now()).count()
        data.append({
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": num_upcoming_shows
        })

    response = {
        "count": len(results),
        "data": data
    }

    return render_template(
        'pages/search_artists.html',
        results=response,
        search_term=search_term, form=form
    )


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id - DONE
    form = SearchForm()

    artist = Artist.query.get(artist_id)

    if not artist:
        return render_template("errors/404.html"), 404

    past_shows = []
    upcoming_shows = []
    current_time = datetime.now()

    if artist.shows:
        for show in artist.shows:
            show_data = {
                "venue_id": show.venue_id,
                "venue_name": show.venue.name,
                "venue_image_link": show.venue.image_link,
                "start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S")
            }
        if show.start_time < current_time:
            past_shows.append(show_data)
        else:
            upcoming_shows.append(show_data)

    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
    }

    return render_template('pages/show_artist.html', artist=data, form=form)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm(obj=artist)

    # TODO: populate form with fields from artist with ID <artist_id> - DONE
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing - DONE
    # artist record with ID <artist_id> using the new attributes
    artist = Artist.query.get(artist_id)
    form = ArtistForm(request.form)

    if form.validate_on_submit():
        try:
            artist.name = form.name.data
            artist.genres = form.genres.data
            artist.city = form.city.data
            artist.state = form.state.data
            artist.phone = form.phone.data
            artist.website = form.website.data
            artist.facebook_link = form.facebook_link.data
            artist.seeking_venue = form.seeking_venue.data
            artist.seeking_description = form.seeking_description.data
            artist.image_link = form.image_link.data

            db.session.commit()
            flash("Artist update " + form.name.data +
                  " was successfully updated.")
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Artist ' + form.name.data + ' could not \
                  be updated.')
            print(f'Error: {e}')
            return render_template(
                'forms/edit_artist.html',
                form=form,
                artist=artist
            )
        finally:
            db.session.close()
    else:
        flash(
            "Form validation failed. Please correct the errors and try again."
        )

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm(obj=venue)
    # TODO: populate form with values from venue with ID <venue_id> - DONE
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing - DONE
    # venue record with ID <venue_id> using the new attributes
    venue = Venue.query.get(venue_id)
    form = VenueForm(request.form)

    if form.validate_on_submit():
        try:
            venue.name = form.name.data
            venue.genres = form.genres.data
            venue.city = form.city.data
            venue.state = form.state.data
            venue.phone = form.phone.data
            venue.website = form.website.data
            venue.facebook_link = form.facebook_link.data
            venue.seeking_talent = form.seeking_talent.data
            venue.seeking_description = form.seeking_description.data
            venue.image_link = form.image_link.data

            db.session.commit()
            flash("Venue update " + form.name.data + " was successful")
        except Exception as e:
            db.session.rollback()
            flash("AN error occured. " + form.name.data + "could not \
                  be updated")
            print(f"Error: {e}")
            return render_template(
                "forms/edit_artist.html",
                form=form,
                venue=venue
            )
        finally:
            db.session.close()
    else:
        flash(
            "Form validation failed. Please correct the errors and try again."
        )

    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead - DONE
    form = ArtistForm(request.form)
    if form.validate_on_submit():
        try:
            new_artist = Artist(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                phone=form.phone.data,
                image_link=form.image_link.data,
                facebook_link=form.facebook_link.data,
                website=form.website.data,
                seeking_venue=form.seeking_venue.data,
                seeking_description=form.seeking_description.data,
                genres=form.genres.data
            )
            db.session.add(new_artist)
            db.session.commit()
            # TODO: modify data to be the data object returned from db insertion
            # on successful db insert, flash success - DONE
            flash('Artist ' + form.name.data + ' was successfully listed!')
            # TODO: on unsuccessful db insert, flash an error instead.
            # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.') - DONE
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Artist ' + form.name.data + ' could not \
                  be listed.')
            print(f'Error: {e}')

        finally:
            db.session.close()
    else:
        print("Form errors:", form.errors)
        flash("Artist form validation failed. Please check the errors and try again.")
    return render_template('forms/new_artist.html', form=form)

#  Shows
#  ----------------------------------------------------------------


@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data. - DONE

    shows = Show.query.all()

    data = []
    for show in shows:
        venue = Venue.query.get(show.venue_id)
        artist = Artist.query.get(show.artist_id)
        data.append({
            "venue_id": venue.id,
            "venue_name": venue.name,
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S")
        })

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing
    # form
    # TODO: insert form data as a new Show record in the db, instead - DONE

    form = ShowForm(request.form)
    if form.validate_on_submit():
        try:
            new_show = Show(
                artist_id=form.artist_id.data,
                venue_id=form.venue_id.data,
                start_time=form.start_time.data,
            )
            db.session.add(new_show)
            db.session.commit()
            # on successful db insert, flash success
            flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead. - DONE
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        except Exception as e:
            db.session.rollback()
            flash("An error occured. Show " + form.show.data + " could not \
              be listed.")
            print(f"Error: {e}")
        finally:
            db.session.close()
    else:
        print("Form errors: ", form.errors)
        flash("Show form validation failed. Please check the errors and try \
              again.")
    return render_template('forms/new_show.html', form=form)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
