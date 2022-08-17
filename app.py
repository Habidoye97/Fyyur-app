#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import sys
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime
from datetime import timedelta
from dateutil import parser
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mayowa1997@localhost:5432/fyyurapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website = db.Column(db.String())
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String())
    genres = db.Column(db.String(120))

    shows = db.relationship('Show', backref='venue', lazy=False, cascade='all, delete-orphan')

    def __repr___(self):
      return f'<Venue id={self.id} name={self.name} city={self.city} state={self.state}>'

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String())
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String())
    
    shows = db.relationship('Show', backref='artist', lazy=False, cascade='all, delete-orphan')

    def __repr__(self):
      return f"<Artist id={self.id} name={self.name} city={self.city} state={self.state}>"


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__= 'show'
  
  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  start_time = db.Column(db.String(120))
  # default=datetime.utcnow
  def __repr__(self):
      return f"<Show id={self.id} name={self.artist_id} city={self.venue_id} state_time={self.start_time}>"


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
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
  
  areas =[]
  distinct_areas = Venue.query.distinct(Venue.city, Venue.state).all()
  for each_area in distinct_areas:
    area ={
      "city": each_area.city,
      "state": each_area.state
    }
    venues_under_area = Venue.query.filter_by(city=each_area.city, state=each_area.state).all()

    # format each venue
    formatted_venues = []
    for venue in venues_under_area:
      formatted_venues.append({
        "id": venue.id,
        "name": venue.name
      })

    area["venues"] = formatted_venues
    areas.append(area)

  data=[{
    "city": "San Francisco",
    "state": "CA",
    "venues": [{
      "id": 1,
      "name": "The Musical Hop",
      "num_upcoming_shows": 0,
    }, {
      "id": 3,
      "name": "Park Square Live Music & Coffee",
      "num_upcoming_shows": 1,
    }]
  }, {
    "city": "New York",
    "state": "NY",
    "venues": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }]
  return render_template('pages/venues.html', areas=areas);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')

  response = {}

  venues = Venue.query.with_entities(Venue.name, Venue.id).all()
  response['data'] = []
  response['count'] = 0
  for venue in venues:
    if venue.name.lower().find(search_term.lower()) != -1:

      venue_unit = {
        "id": venue.id,
        "name": venue.name,

      }
      response["data"].append(venue_unit) 
      response['count'] = response['count'] + 1

  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  list_of_shows_venue = db.session.query(Venue, Show).join(Show).filter(Venue.id==venue_id).all()

  # venue = Venue.query.filter_by(id=venue_id).first()
  # list_of_shows_in_venue = Show.query.filter_by(venue_id=venue_id).all()
  past_shows = []
  upcoming_shows =[]
  today = datetime.now() - timedelta(days=0)
  
  for show in list_of_shows_venue:
    time = parser.parse(show.Show.start_time)
    if time.replace(tzinfo=None) < today.replace(tzinfo=None):
      past_show = {
        "artist_id": show.Show.artist.id,
        "artist_name": show.Show.artist.name,
        "artist_image_link": show.Show.artist.image_link,
        "start_time": show.Show.start_time
      }
      past_shows.append(past_show)
    else:
      upcoming_show = {
        "artist_id": show.Show.artist.id,
        "artist_name": show.Show.artist.name,
        "artist_image_link": show.Show.artist.image_link,
        "start_time": show.Show.start_time
      }
      upcoming_shows.append(upcoming_show)

  venuedata ={
    "id": list_of_shows_venue[0].Venue.id,
    "name": list_of_shows_venue[0].Venue.name,
    "genres": list(list_of_shows_venue[0].Venue.genres.split(",")),
    "address": list_of_shows_venue[0].Venue.address,
    "city": list_of_shows_venue[0].Venue.city,
    "state": list_of_shows_venue[0].Venue.state,
    "phone": list_of_shows_venue[0].Venue.phone,
    "website": list_of_shows_venue[0].Venue.website,
    "facebook_link": list_of_shows_venue[0].Venue.facebook_link,
    "seeking_talent": list_of_shows_venue[0].Venue.seeking_talent,
    "seeking_description": list_of_shows_venue[0].Venue.seeking_description,
    "image_link": list_of_shows_venue[0].Venue.image_link,
    "past_shows": past_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows": upcoming_shows,
    "upcoming_shows_count": len(upcoming_shows)
  }
  
  return render_template('pages/show_venue.html', venue=venuedata)

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
  venue_form = VenueForm(request.form)
  if venue_form.validate():
    try:
      new_venue = Venue(
        name=venue_form.name.data,
        genres=','.join(venue_form.genres.data),
        address=venue_form.address.data,
        city=venue_form.city.data,
        state=venue_form.state.data,
        phone=venue_form.phone.data,
        facebook_link=venue_form.facebook_link.data,
        image_link=venue_form.image_link.data,
        website=venue_form.website_link.data,
        seeking_talent=venue_form.seeking_talent.data,
        seeking_description=venue_form.seeking_description.data
      )
      db.session.add(new_venue)
      db.session.commit()
      db.session.close()
      # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except: 
      db.session.rollback()
      
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
      print(sys.exc_info())
    finally:
      db.session.close()
  else:
    print("\n\n", venue_form.errors)
    flash("Venue was not created successfully.")
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>/delete', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    venue = Venue.query.filter_by(id=venue_id)
    venue_show = Show.query.filter_by(venue_id=venue.id).all()
    for show in venue_show:
      db.session.delete(show)
    db.session.delete(venue)
    db.session.commit()
    flash("Venue " + venue.name + "was deleted successfully")
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash("Venue was not deleted")
  finally:
    db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for("index"))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data=[{
    "id": 4,
    "name": "Guns N Petals",
  }, {
    "id": 5,
    "name": "Matt Quevedo",
  }, {
    "id": 6,
    "name": "The Wild Sax Band",
  }]
  return render_template('pages/artists.html', artists=Artist.query.all())

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')

  response= {}

  artists = Artist.query.with_entities(Artist.name, Artist.id).all()
  response['data'] = []
  response['count'] = 0
  for artist in artists:
    if artist.name.lower().find(search_term.lower()) != -1:

      artist_unit = {
        "id": artist.id,
        "name": artist.name,

      }
      response["data"].append(artist_unit) 
      response['count'] = response['count'] + 1

  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  list_of_shows_artist = db.session.query(Artist, Show).join(Show).filter(Artist.id==artist_id).all()
  artist = Artist.query.filter_by(id=artist_id).first()

  list_of_shows_by_artist = Show.query.filter_by(artist_id=artist_id).all()
  past_shows = []
  upcoming_shows =[]
  today = datetime.now() - timedelta(days=0)
  
  for show in list_of_shows_artist:
    time = parser.parse(show.Show.start_time)
    if time.replace(tzinfo=None) < today.replace(tzinfo=None):
      past_show = {
        "venue_id": show.Show.venue.id,
        "venue_name": show.Show.venue.name,
        "venue_image_link": show.Show.venue.image_link,
        "start_time": show.Show.start_time
      }
      past_shows.append(past_show)
    else:
      upcoming_show = {
        "venue_id": show.Show.venue.id,
        "venue_name": show.Show.venue.name,
        "venue_image_link": show.Show.venue.image_link,
        "start_time": show.Show.start_time
      }
      upcoming_shows.append(upcoming_show)
  artistdata ={
    "id": artist.id,
    "name": artist.name,
    "genres": list(artist.genres.split(",")),
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website_link,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows": upcoming_shows,
    "upcoming_shows_count": len(upcoming_shows)
  }
  
  # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=artistdata)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.filter_by(id= artist_id).first()
  # artist={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  # }
  # TODO: populate form with fields from artist with ID <artist_id>
  form.genres.data = artist.genres.split(",")
  form.name.data  = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.website_link.data = artist.website_link
  form.facebook_link.data = artist.facebook_link
  form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data = artist.seeking_description
  form.image_link.data = artist.image_link
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm(request.form)

  if form.validate():
    try: 
      artist = Artist.query.filter_by(id=artist_id).first()
      artist.name = form.name.data
      artist.genres = ','.join(form.genres.data)
      artist.city = form.city.data
      artist.state = form.state.data
      artist.phone = form.phone.data
      artist.website_link = form.website_link.data
      artist.facebook_link = form.facebook_link.data
      artist.seeking_venue = form.seeking_venue.data
      artist.seeking_description = form.seeking_description.data
      artist.image_link = form.image_link.data
          
          # db.session.add(artist)
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully updated')
    except: 
      db.session.rollback()
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
    finally:
      db.session.close()
  else:
    print("\n\n", form.errors)
    flash("Artist was not successfully updated.")
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.filter_by(id=venue_id).first()
  # venue={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  # }
  # TODO: populate form with values from venue with ID <venue_id>
  form.genres.data = venue.genres.split(",")
  form.name.data  = venue.name
  form.address.data = venue.address
  form.city.data = venue.city
  form.state.data = venue.state
  form.phone.data = venue.phone
  form.website_link.data = venue.website
  form.facebook_link.data = venue.facebook_link
  form.seeking_talent.data = venue.seeking_talent
  form.seeking_description.data = venue.seeking_description
  form.image_link.data = venue.image_link
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existin       g
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm(request.form)
  if form.validate():
    try: 
      venue = Venue.query.filter_by(id=venue_id).first()
      venue.name = form.name.data
      venue.genres = ','.join(form.genres.data)
      venue.address = form.address.data 
      venue.city = form.city.data
      venue.state = form.state.data
      venue.phone = form.phone.data
      venue.website = form.website_link.data 
      venue.facebook_link = form.facebook_link.data
      venue.seeking_talent = form.seeking_talent.data
      venue.seeking_description = form.seeking_description.data
      venue.image_link = form.image_link.data
      
      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully updated')
    except: 
      db.session.rollback()
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
    finally:
      db.session.close()
  else:
    print("\n\n", form.errors)
    flash("Venue was not successfully updated.")
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
  artist_form = ArtistForm(request.form)

  try:
    new_artist = Artist(name=artist_form.name.data,
        genres=','.join(artist_form.genres.data),
        city=artist_form.city.data,
        state=artist_form.state.data,
        phone=artist_form.phone.data,
        facebook_link=artist_form.facebook_link.data,
        image_link=artist_form.image_link.data,
        website_link=artist_form.website_link.data,
        seeking_venue=artist_form.seeking_venue.data,
        seeking_description=artist_form.seeking_description.data
    )
    db.session.add(new_artist)
    db.session.commit()
      
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except: 
    db.session.rollback()
    
    flash('An error occurred. Artist' + request.form['name'] + ' could not be listed.')
    
  finally:
    db.session.close()
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  show_list=[]
  shows = Show.query.all()
  for show in shows:
    show_unit= {
      "venue_id": show.venue.id,
      "venue_name": show.venue.name,
      "artist_id": show.artist.id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time
    }

    show_list.append(show_unit)
    
  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]
  return render_template('pages/shows.html', shows=show_list)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  show_form = ShowForm(request.form)
  if show_form.validate():
    try:
    
      new_show = Show(
          venue_id = show_form.venue_id.data,
          artist_id = show_form.artist_id.data,
          start_time = show_form.start_time.data
      )
      db.session.add(new_show)
      db.session.commit()
        # on successful db insert, flash success
      flash('Show was successfully listed!')
    except:
      db.session.rollback()
      flash('An error occurred, Show was not added')

    finally:
      db.session.close()
  else:
    print("\n\n", show_form.errors)
    flash('An error occurred, Show was not added')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

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
