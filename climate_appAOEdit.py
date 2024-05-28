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

    results = session.query(measurement.date, measurement.prcp).filter(measurement.date > '2016-02-23').all()

    session.close()

    precip_data = []

    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precip_data.append(precip_dict)
    return jsonify(precip_data)

##3. Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
    session = session(engine)

    results = session.query(measurement.station).distinct().all()
      
    session.close()

    station_data = []
    for station in results:
        station_dict = {}
        station_dict["station name"] = station[0]
        station_data.append(station_dict)
    return jsonify(station_data)

##4. Query the dates and temperature observations of the most-active station for the previous year of data.
##Return a JSON list of temperature observations for the previous year.  

@app.route("/api/v1.0/tobs")      
def tobs():
    session = session(engine)
    
    results = session.query(measurement.tobs).filter(measurement.station=='USC00519281').filter(measurement.date>='2016-08-23').all()

    session.close()

    tobs_data = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["Observed Temperature"] = tobs
        tobs_data.append(tobs_dict)
    return jsonify(tobs_data)

##5. Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
## For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
## For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive

@app.route("/api/v1.0/<start_date>")
def temps_start(start):
    session = session(engine)

    results = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.date >= start).all()

    session.close()

    temp = []
    for min_temp, avg_temp, max_temp in results:
        temps_dict = {}
        temps_dict['Minimum Temperature'] = min_temp
        temps_dict['Average Temperature'] = avg_temp
        temps_dict['Maximum Temperature'] = max_temp
        temps.append(temps_dict)
    return jsonify(temps)

@app.route("/api/v1.0/<start_date>/<end>")
def temps_start_end(start, end):
    session = session(engine)

    results = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <=end).all()

    session.close()

    temp = []
    for min_temp, avg_temp, max_temp in results:
        temps_dict = {}
        temps_dict['Minimum Temperature'] = min_temp
        temps_dict['Average Temperature'] = avg_temp
        temps_dict['Maximum Temperature'] = max_temp
        temps.append(temps_dict)
    return jsonify(temps)

if __name__ == '__main__':
    app.run(debug=True)