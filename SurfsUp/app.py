# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurements = Base.classes.measurement
Stations = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Home Page
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start (enter as YYYY-MM-DD)<br/>"
        f"/api/v1.0/start/end (enter as YYYY-MM-DD/YYYY-MM-DD)"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the JSON representation of a dictionary using 'date' as the key and 'prcp' as the value for the last year"""
    # Starting from the most recent data point in the database.
    most_recent_date = dt.date(2017, 8, 23)
    # Calculate the date one year from the last date in data set.
    first_date = most_recent_date - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurements.date, Measurements.prcp).\
        filter(Measurements.date >= first_date).all()
    
    # Close the session
    session.close()

    # Create an empty list
    precip_list = []

    # For loop to add precip_data to a dictionary
    for date, precip in results:
        precip_dict = {}
        precip_dict['date'] = date
        precip_dict['precipitation'] = precip
        precip_list.append(precip_dict)
    
    # jsonify the list
    return jsonify(precip_list)

# @app.route("/api/v1.0/stations")
# def stations():

if __name__ == '__main__':
    app.run(debug=True)