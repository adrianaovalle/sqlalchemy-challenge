import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Calculate last date and date 1 year ago from the last data point
session = Session(engine)
last_date= dt.date(int(max(session.query(Measurement.date).all())[0][:4]), 
                   int(max(session.query(Measurement.date).all())[0][5:7]), 
                   int(max(session.query(Measurement.date).all())[0][8:]))
target_date=last_date-dt.timedelta(days=365)
session.close()
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    
    return (
        f"Welcome to the Honololu, Hawaii Climate App!<br/>"
        f"  <br/>"
        f"Available Routes:<br/>"
        f"  <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        f"  <br/>"
        f"  <br/>"
        f"Note: Replace start by start date in format: YYYY-MM-DD<br/>"
        f"      and Replace end by end date in format: YYYY-MM-DD<br/>"

    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the last 12 months precipitation
    OneYear_Precip=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= target_date).\
                order_by(Measurement.date).all()
    session.close()

    # Convert list of tuples into normal list
    precip = []
    for date, prcp in OneYear_Precip:
        p_dict = {}
        p_dict["Date"] = date
        p_dict["Precipitation"] = prcp
        precip.append(p_dict)

    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query list of stations
    list_stations=session.query(Station.station).all()
    session.close()

    # Convert list of tuples into normal list
    stations = list(np.ravel(list_stations))

    return jsonify(stations)
 
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query most active station
    most_temp=session.query(Measurement.station,func.count(Measurement.id)).\
                    group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).all()
    most_temp_station=most_temp[0][0]
    
    # Query the last 12 months of temperature observation data for this station 
    year_temps=session.query(Measurement.tobs).filter(Measurement.station==most_temp_station).\
        filter(Measurement.date >= target_date).order_by(Measurement.date).all()
    
    session.close()

    # Convert list of tuples into normal list
    temp = list(np.ravel(year_temps))

    return jsonify(temp)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temps(start=None, end=None):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        end=last_date
        end=end.strftime("%Y-%m-%d")
    
    # Query temperatures for date range
    results=session.query(*sel).filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    session.close()

    # Make list of dictionnaries
    return_list = []
    date_dict = {'start_date': start,'end_date': end}
    return_list.append(date_dict)
    return_list.append({'Observation': 'Min. Temperature', 'Temperature': round(results[0][0],2)})
    return_list.append({'Observation': 'Avg. Temeperature', 'Temperature': round(results[0][1],2)})
    return_list.append({'Observation': 'Max. Temperature', 'Temperature': round(results[0][2],2)})
    return jsonify(return_list)

if __name__ == '__main__':
    app.run(debug=True)
