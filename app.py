# Import the dependencies.
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from pathlib import Path

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
# Save references to each table
Measurement = Base.classes.measurement
Station=Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/start <br/>"
        f"/api/v1.0/start/end"
        )

@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of prcp"""
    # returns json with the date as the key and the value as the precipitation 
    Year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    precipitation_scores=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= Year_ago).all()
    session.close()
    
    all_prcp = {}
    for date, prcp in precipitation_scores:
        all_prcp [date] = prcp
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)
     # returns json with the station as a list
    """Return a list of all station"""
    stations_list=session.query(Station.station).all()
    session.close()
    stations = list(np.ravel(stations_list))
    return jsonify(stations)  
    

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # returns json with the tob and date as a list 
    """Return a list of all tobs"""
    Year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    tob_data=session.query(Measurement.date,Measurement.tobs).\
    filter(Measurement.date >= Year_ago).filter(Measurement.station == 'USC00519281').all()
    session.close()

    tob_list = list(np.ravel(tob_data))
    return jsonify(tob_list)  
    

@app.route("/api/v1.0/<start>")
def stats(start):
    # Create our session (link) from Python to the DB
    start=dt.datetime.strptime(start,"%Y%m%d")
    session = Session(engine)
    # returns json with the min , max, avg of tob and via start filter
    """Return a list of all min max avg tobs"""
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date>= start).all()
    session.close()
    all_temps = list(np.ravel(results))
    return jsonify(all_temps) 

@app.route("/api/v1.0/<start>/<end>")
def stats2(start,end):
    # Create our session (link) from Python to the DB
    start=dt.datetime.strptime(start,"%Y%m%d")
    end=dt.datetime.strptime(end,"%Y%m%d")
    session = Session(engine)
    # returns json with the min , max, avg of tob and via start and end filter
    """Return a list of all min max avg tobs"""
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    all_temps2 = list(np.ravel(results))
    return jsonify(all_temps2)    


if __name__ == "__main__":
    app.run(debug=True)
