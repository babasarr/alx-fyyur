#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from ast import For
from curses import echo
import json
from typing import Any
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for,jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_migrate import Migrate
from flask_wtf import Form
from forms import *
from models import Show,Venue,Artist


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)




# TODO: connect to a local postgresql database


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  #date = dateutil.parser.parse(value)
  date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
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
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
 
  data = db.session.query(Venue.city,Venue.state).group_by(Venue.city,Venue.state).all()

  for da in data:
    da.venues = Venue.query.get(city=da.city).all()

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"


  data = request.form.get('search_term', '')

  response = db.session.query(Venue).filter(Venue.name.ilike(data))

  setattr(response, "count", response.count() )  
  setattr(response, "data", response.all() )   

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data = Venue.query.get(venue_id)
  data.genres = "genres", data.genres.split(",")
  past_shows =  filter(lambda show: show.start_time <= datetime.now(), data.shows) 
  upcoming_shows = filter(lambda show: show.start_time > datetime.now(), data.shows) 

  setattr(data, "past_shows",past_shows)  
  setattr(data, "upcoming_shows",upcoming_shows)  
  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = VenueForm(request.form)

  try:
      name = form.name.data
      city = form.city.data
      state = form.state.data
      address = form.address.data
      phone = form.phone.data
      image_link = form.image_link.data
      facebook_link = form.facebook_link.data
      genres = form.genres.data
      website_link = form.website_link.data
      seeking_talent = form.seeking_talent.data
      seeking_description = form.seeking_description.data

      venue = Venue(name=name,city=city,state=state,address=address,phone=phone,image_link=image_link,facebook_link=facebook_link,genres=genres,website_link=website_link,seeking_talent=seeking_talent,seeking_description=seeking_description)
      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
      db.session.rollback()
     
      flash('An error occurred. Venue ' + request.form['name']  + ' could not be listed.') 
  finally:
      db.session.close()
  
  return render_template('pages/home.html')

  # on successful db insert, flash success
  # flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  # return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  try:        
      venue = Venue.query.get(venue_id)
      db.session.delete(venue)
      db.session.commit()
  except:
      db.session.rollback()
      return None
  finally:
      db.session.close()
  return jsonify({ 'success': True })
  

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.order_by('id').all()

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  
  data = request.form.get('search_term', '')

  response = db.session.query(Artist).filter(Artist.name.ilike(data))

  setattr(response, "count", response.count() )  
  setattr(response, "data", response.all() )  

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  
  data = Artist.query.get(artist_id)
  data.genres = "genres", data.genres.split(",")
  past_shows =  filter(lambda show: show.start_time <= datetime.now(), data.shows) 
  upcoming_shows = filter(lambda show: show.start_time > datetime.now(), data.shows) 

  setattr(data, "past_shows",past_shows)  
  setattr(data, "upcoming_shows",upcoming_shows)  
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

  # TODO: populate form with fields from artist with ID <artist_id>

  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.image_link.data = artist.image_link
  form.facebook_link.data = artist.facebook_link
  form.genres.data = artist.genres
  form.website_link.data = artist.website_link
  form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data = artist.seeking_description

  
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  artist = Artist.query.get(artist_id)
  form = ArtistForm(request.form)
  try:
      artist.name = form.name.data
      artist.city = form.city.data
      artist.state = form.state.data
      artist.phone = form.phone.data
      artist.image_link = form.image_link.data
      artist.facebook_link = form.facebook_link.data
      artist.genres = form.genres.data
      artist.website_link = form.website_link.data
      artist.seeking_venue = form.seeking_venue.data
      artist.seeking_description = form.seeking_description.data

      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully update!')
  except:
      db.session.rollback()
      flash('An error occurred. Artist ' + request.form['name']+ ' could not be update.')  
  finally:
      db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  # TODO: populate form with values from venue with ID <venue_id>

  venue = Venue.query.get(venue_id)
  form = VenueForm()
  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.address.data = venue.address
  form.phone.data = venue.phone
  form.image_link.data = venue.image_link
  form.facebook_link.data = venue.facebook_link
  form.genres.data = venue.genres
  form.website_link.data = venue.website_link
  form.seeking_talent.data = venue.seeking_talent
  form.seeking_description.data = venue.seeking_description

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue = Venue.query.get(venue_id)
  form = VenueForm(request.form)
  try:
    venue.name = form.name.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.address = form.address.data
    venue.phone = form.phone.data
    venue.image_link = form.image_link.data
    venue.facebook_link = form.facebook_link.data
    venue.genres = form.genres.data
    venue.website_link = form.website_link.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data

    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully updated!')
  except:
      error = True
      db.session.rollback()
      flash('An error occurred. Venue ' + request.form['name']+ ' could not be updated.')  
  finally:
      db.session.close()

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
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm(request.form)
  try:
      name = form.name.data
      city = form.city.data
      state = form.state.data
      phone = form.phone.data
      image_link = form.image_link.data
      facebook_link = form.facebook_link.data
      genres = form.genres.data
      website_link = form.website_link.data
      seeking_venue = form.seeking_venue.data
      seeking_description = form.seeking_description.data

      artist = Artist(name=name,city=city,state=state,phone=phone,image_link=image_link,facebook_link=facebook_link,genres=genres,website_link=website_link,seeking_venue=seeking_venue,seeking_description=seeking_description)
      db.session.add(artist)
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
      db.session.rollback()
      flash('An error occurred. Artist ' + request.form['name']+ ' could not be listed.')  
  finally:
      db.session.close()
  
  return render_template('pages/home.html')

  # on successful db insert, flash success
  #flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.

  data = Show.query.order_by('id').all()
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  
  form = ShowForm(request.form)
  try:
      venue_id = form.venue_id.data
      artist_id = form.artist_id.data
      start_time = form.start_time.data 
      
      show = Show(venue_id=venue_id, artist_id=artist_id, start_time=start_time)
      db.session.add(show)
      db.session.commit()
      flash('Show was successfully listed!')
  except:
      flash('An error occurred. Show could not be listed.')
  finally:
      db.session.close()
  
  return render_template('pages/home.html')

  # on successful db insert, flash success
  # flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  #return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
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
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
