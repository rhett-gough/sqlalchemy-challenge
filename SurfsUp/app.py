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
        f"Welcome to the Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start (enter start as YYYY-MM-DD)<br/>"
        f"/api/v1.0/start/end (enter start/end as YYYY-MM-DD/YYYY-MM-DD)"
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

    # Create a dictionary to add data to
    precip_dict = {}

    # For loop to add precip_data to a dictionary
    for date, precip in results:
        if date not in precip_dict:
            precip_dict[date] = []
        precip_dict[date].append(precip)
    
    # jsonify the list
    return jsonify(precip_dict)

# Station Page
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset."""

    #Perform a query to retrieve the list of Station names
    results = session.query(Stations.name).all()

    #Close the session
    session.close()

    # Create a list for the stations
    station_list = list(np.ravel(results))

    # jsonify the list
    return jsonify(station_list)

# Temperature Page
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Query the dates and temperature observations of the most-active station for the previous year of data.
    Return a JSON list of temperature observations for the previous year."""

    #Perform a query to retrieve the the last 12 months of temperature observation data for this station and plot the results as a histogram
    # Starting from the most recent data point in the database.
    most_recent_date_station = dt.date(2017, 8, 18)

    # Calculate the date one year from the last date in data set.
    first_date_station = most_recent_date_station - dt.timedelta(days=365)

    # Perform a query to retrieve the temperature scores
    results = session.query(Measurements.date, Measurements.tobs).\
        filter(Measurements.date >= first_date_station).\
        filter(Measurements.station == 'USC00519281').all()
    
    # Close the session
    session.close()

    # Create a dictionary for the list of dates and temperatures for the station
    station_temps_dict = {}

    # Use a for loop to populate the dictionary
    for date, temp in results:
        station_temps_dict[date] = temp

    return jsonify(station_temps_dict)

# Summary Stats Start page
@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start date"""

    # Get min, max, and average temp
    function_results = session.query(func.min(Measurements.tobs), func.max(Measurements.tobs), func.avg(Measurements.tobs)).\
        filter(Measurements.date >= start).first()

    # End the session
    session.close()

    # Extract the results
    (TMIN, TMAX, TAVG) = function_results

    # Add them to a dictionary
    temp_stats = {}
    temp_stats['Minimum Temperature'] = TMIN
    temp_stats['Maximum Temperature'] = TMAX
    temp_stats['Average Temperature'] = TAVG

    # return the results  
    return jsonify(temp_stats)

# Summary Stats Start and End page
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start and end date"""

    # Get min, max, and average temp
    function_results = session.query(func.min(Measurements.tobs), func.max(Measurements.tobs), func.avg(Measurements.tobs)).\
        filter(Measurements.date >= start).\
        filter(Measurements.date <= end).first()

    # End the session
    session.close()

    # Extract the results
    (TMIN, TMAX, TAVG) = function_results

    # Add them to a dictionary
    temp_stats = {}
    temp_stats['Minimum Temperature'] = TMIN
    temp_stats['Maximum Temperature'] = TMAX
    temp_stats['Average Temperature'] = TAVG

    # Return the results    
    return jsonify(temp_stats)

# Debugger to close the app
if __name__ == '__main__':
    app.run(debug=True)