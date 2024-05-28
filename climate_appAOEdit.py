#climate app

# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt


#################################################
# Database Setup
#################################################

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()
# reflect the tables
base.prepare(autoload_with=engine)

# Save references to each table
measurement = base.classes.measurement
station = base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

#flask setup
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return(f"Available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/<start><br/>"
            f"/api/v1.0/<start>/<end><br/>"
            )

##2. Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
##Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitatin():
        session = session(engine)

        precip_analysis = session.query(measurement.date, measurement.prcp).filter(measurement.date > '2016-02-23').all()

        session.close()

        precip_data = []

        for date, prcp in precip_analysis:
              precip_dict = {}
              precip_dict["date"] = date
              precip_dict["prcp"] = prcp
              precip_data.append(precip_dict)
        return jsonify(precip_data)

##3. Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
        session = session(engine)

        station_list = session.query(measurement.station).distinct().all()
      
        session.close()

        station_data = []
        for station in station_list:
            station_dict = {}
            station_dict["station name"] = station[0]
            station_data.append(station_dict)
        return jsonify(station_data)

  
        