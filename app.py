# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template,\
  request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from datetime import datetime
from model import db, Venue, Artist, Show, setup_db
# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
setup_db(app)

# TODO: connect to a local postgresql database

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#
# Date formatter for the frontend


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#
# route handler for the homepage


@app.route('/')
def index():
    return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------
# route handler for /venues


@app.route('/venues')
def venues():
    venues = Venue.query.all()
    # DONE: replace with real venues data.
    # num_shows should be aggregated based
    # on number of upcoming shows per venue.

    data = []
    for venue in venues:
        data.append({
            "city": venue.city,
            "state": venue.state,
            "venues": [{
                "id": venue.id,
                "name": venue.name
                }]
        })
    return render_template('pages/venues.html', areas=data)

# Venue Search


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # DONE: implement search on artists with partial
    # string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop"
    # and "Park Square Live Music & Coffee"
    name = request.form.get('search_term')
    search_term = "%{}%".format(name)
    venues = Venue.query.filter(Venue.name.ilike(search_term)).all()

    data = []
    if venues:
        for venue in venues:
            data.append({
                "id": venue.id,
                "name": venue.name,
            })

    response = {
        "count": len(venues),
        "data": data
    }
    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


# GET venue by id
@app.route('/venues/<int:venue_id>', methods=['GET'])
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id

    shows = Show.query.filter(Show.venue == venue_id).all()
    venue = Venue.query.get(venue_id)
    past_shows = []
    upcoming_shows = []
    for show in shows:
        if(shows and datetime.now() > show.start_time):
            past_shows.append({
                "artist_id": show.Artist.id,
                "artist_name": show.Artist.name,
                "artist_image_link": show.Artist.image_link,
                "start_time": str(show.start_time)
            })
        else:
            upcoming_shows.append({
                "artist_id": show.Artist.id,
                "artist_name": show.Artist.name,
                "artist_image_link": show.Artist.image_link,
                "start_time": str(show.start_time)
            })
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
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template('pages/show_venue.html', venue=data)

# Create Venue
# ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm()
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    if request.method == 'POST':
        try:
            venue = Venue(
                  name=form.name.data,
                  city=form.city.data,
                  state=form.state.data,
                  address=form.address.data,
                  genres=form.genres.data,
                  phone=form.phone.data,
                  website=form.website.data,
                  image_link=form.image_link.data,
                  facebook_link=form.facebook_link.data
                )

            db.session.add(venue)
            db.session.commit()

            # on successful db insert, flash success
            flash('Venue ' + form.name.data + ' was successfully listed!')
        except:
            db.session.rollback()

            # DONE: on unsuccessful db insert, flash an error instead.
            flash('An error occurred. Venue ' +
                  form.name.data + ' could not be listed.')
        finally:
            db.session.close()
            return render_template('pages/home.html')

#  DELETE
# DELETE a Venue by id


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # DONE: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record.
    # Handle cases where the session commit could fail.
    venue = Venue.query.get(venue_id)
    if venue and request.method == 'DELETE':
        try:
            db.session.delete(venue)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()
            # BONUS CHALLENGE: Implement a button to delete a
            # Venue on a Venue Page, have it so that
            # clicking that button delete it from the db
            # then redirect the user to the homepage
            return render_template('pages/home.html')

# DELETE an Artist by id


@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    # DONE: Complete this endpoint for taking a artist_id, and using
    # SQLAlchemy ORM to delete a record.
    # Handle cases where the session commit could fail.
    artist = Artist.query.get(artist_id)
    if artist and request.method == 'DELETE':
        try:
            db.session.delete(artist)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()
            '''
            BONUS CHALLENGE: Implement a button to delete a
            Venue on a Venue Page, have it so that
            clicking that button delete it from the db then
            redirect the user to the homepage
            '''
            return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
# GET list of artists


@app.route('/artists')
def artists():
    # DONE: replace with real data returned from querying the database
    artists = Artist.query.all()
    data = []

    for artist in artists:
        data.append({
            'id': artist.id,
            'name': artist.name
        })

    return render_template('pages/artists.html', artists=data)

# POST artists/search


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # DONE: implement search on artists with partial string search.
    # Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals",
    # "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".

    name = request.form.get('search_term')
    search_term = "%{}%".format(name)
    artists = Artist.query.filter(Artist.name.ilike(search_term)).all()

    data = []
    if artists:
        for artist in artists:
            data.append({
                "id": artist.id,
                "name": artist.name,
            })

    response = {
        "count": len(artists),
        "data": data
    }
    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))

# GET an artist


@app.route('/artists/<int:artist_id>', methods=['GET'])
def show_artist(artist_id):
    '''
    shows the artist page with the given artist_id
    DONE: replace with real artist data from the
    artists table, using artist_id
    '''
    shows = Show.query.filter(Show.artist == artist_id).all()
    artist = Artist.query.get(artist_id)
    past_shows = []
    upcoming_shows = []
    for show in shows:
        if(shows and datetime.now() > show.start_time):
            past_shows.append({
                "venue_id": show.Venue.id,
                "venue_name": show.Venue.name,
                "venue_image_link": show.Venue.image_link,
                "start_time": str(show.start_time)
            })
        else:
            upcoming_shows.append({
                "venue_id": show.Venue.id,
                "venue_name": show.Venue.name,
                "venue_image_link": show.Artist.image_link,
                "start_time": str(show.start_time)
            })
    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template('pages/show_artist.html', artist=data)

# Update
# ----------------------------------------------------------------
# Fetch Artist Update Form into view


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    # DONE: populate form with fields from artist with ID <artist_id>

    form.name.data = artist.name
    form.city.data = artist.city
    form.phone.data = artist.phone
    form.facebook_link.data = artist.facebook_link
    form.image_link.data = artist.image_link

    return render_template('forms/edit_artist.html', form=form, artist=artist)

# Artist Update Controller


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # DONE: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    form = ArtistForm()
    artist = Artist.query.get(artist_id)

    if artist:
        try:
            artist.name = form.name.data
            artist.city = form.city.data
            artist.phone = form.phone.data
            artist.state = form.state.data
            artist.genres = form.genres.data
            artist.facebook_link = form.facebook_link.data
            artist.image_link = form.image_link.data

            db.session.commit()
            flash('Artist ' + form.name.data + ' was successfully Updated!')
        except:
            db.session.rollback()
            flash('Artist ' + form.name.data + ' could not be  Updated!')
        finally:
            db.session.close()
            return redirect(url_for('show_artist', artist_id=artist_id))

# Fetch Venue Update Form into view


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)

    form.name.data = venue.name
    form.address.data = venue.address
    form.city.data = venue.city
    form.phone.data = venue.phone
    form.facebook_link.data = venue.facebook_link
    form.image_link.data = venue.image_link
    form.website.data = venue.website
    # DONE: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)

# Venue Update Controller


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    if venue:
        try:
            venue.name = form.name.data
            venue.city = form.city.data
            venue.state = form.state.data
            venue.phone = form.phone.data
            venue.facebook_link = form.facebook_link.data
            venue.image_link = form.image_link.data
            venue.website = form.website.data

            db.session.commit()
            flash('Venue ' + form.name.data +
                  ' was successfully Updated!')
        except:
            db.session.rollback()
        finally:
            db.session.close()
            return redirect(url_for('show_venue', venue_id=venue_id))

# Create Artist
# ----------------------------------------------------------------
# Fetch Artist Create Form


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


# Artist Create Controller
@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    form = ArtistForm()
    # DONE: insert form data as a new Artist record in the db, instead
    # DONE: modify data to be the data object returned from db insertion
    if request.method == 'POST':
        try:
            artist = Artist(
                    name=form.name.data,
                    city=form.city.data,
                    state=form.state.data,
                    genres=form.genres.data,
                    phone=form.phone.data,
                    image_link=form.image_link.data,
                    facebook_link=form.facebook_link.data
                    )

            db.session.add(artist)
            db.session.commit()

            # on successful db insert, flash success
            flash('Artist ' + form.name.data +
                  ' was successfully listed!')
        except:
            db.session.rollback()
            # DONE: on unsuccessful db insert, flash an error instead.
            flash('An error occurred. Artist ' + form.name.data +
                  ' could not be listed.')

        finally:
            db.session.close()
            return render_template('pages/home.html')


# Shows
# ----------------------------------------------------------------
# Fetch list of shows
@app.route('/shows')
def shows():
    '''
    displays list of shows at /shows
    DONE: replace with real venues data.
    num_shows should be aggregated based on number of upcoming shows per venue.
    '''
    shows = Show.query.all()
    data = []
    if shows:
        for show in shows:
            data.append({
                "venue_id": show.Venue.id,
                "venue_name": show.Venue.name,
                "artist_id": show.Artist.id,
                "artist_name": show.Artist.name,
                "artist_image_link": show.Artist.image_link,
                "start_time": str(show.start_time)
            })

    return render_template('pages/shows.html', shows=data)

# Fetch form for creating a Show


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

# Create a Show


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    '''
    called to create new shows in the db,
    upon submitting new show listing form
    TODO: insert form data as a new Show record in the db, instead
    '''
    form = ShowForm()
    if request.method == 'POST':
        try:
            show = Show(
                venue=form.venue_id.data,
                artist=form.artist_id.data,
                start_time=form.start_time.data
            )

            db.session.add(show)
            db.session.commit()
            # on successful db insert, flash success
            flash('Show was successfully listed!')

        except:
            db.session.rollback()
            # DONE: on unsuccessful db insert, flash an error instead.
            # e.g., flash('An error occurred. Show could not be listed.')
            # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
            flash('An error occurred. Show could not be listed.')

        finally:
            db.session.close()
            return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(Formatter('% (asctime)s % (levelname)s:
                              % (message)s[in % (pathname)s: % (lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
