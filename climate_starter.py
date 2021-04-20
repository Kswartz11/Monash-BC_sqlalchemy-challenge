import numpy as np
import datetime as dt
import pandas as pd 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to measurement table
measmt = Base.classes.measurement

# Save references to station table
statn = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

################################################################################################################
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

################################################################################################################ 
@app.route("/api/v1.0/precipitation")
def precipitiation():
    
    session = Session(engine)
   
    measmt_results = session.query(measmt.date, measmt.prcp).all()

    session.close()
   
    prcp_data = []
    for date, prcp in measmt_results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)


############################################################################################################## 
@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)
    
    statn_results = session.query(measmt.station, measmt.tobs).all()

    session.close()
   
    tobs_data = []
    for station, tobs in statn_results:
        tobs_dict = {}
        tobs_dict["station"] = station
        tobs_dict["tobs"] = tobs
        tobs_data.append(tobs_dict)

    return jsonify(tobs_data)
     
#################################################################################################################### 
@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
      
    USC00519281_results = session.query(measmt.station, measmt.tobs).\
    filter(measmt.station == 'USC00519281').\
    order_by(measmt.station).all()

    session.close()

    USC00519281_list = []
    
    for date, tobs in USC00519281_results:
        USC00519281_dict = {}
        USC00519281_dict["date"] = date
        USC00519281_dict["tobs"] = tobs
        USC00519281_list.append(USC00519281_dict)

    return jsonify(USC00519281_list)

################################################################################################################# 
@app.route("/api/v1.0/<start>")
def tobs_start(start):

    
    session = Session(engine)

    end = session.query(measmt.date).order_by(measmt.date.desc()).first()
    start = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    tobs_query = session.query(func.min(measmt.tobs), func.avg(measmt.tobs), func.max(measmt.tobs)).\
        filter(measmt.date >= start).all()

    session.close()

    tobs_list = []

    for min,avg,max in tobs_query:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

###############################################################################################################
@app.route("/api/v1.0/<start>/<end>")
def tobs_start_end(start):

    
    session = Session(engine)

    end = session.query(measmt.date).order_by(measmt.date.desc()).first()
    start = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    tobs_query = session.query(func.min(measmt.tobs), func.avg(measmt.tobs), func.max(measmt.tobs)).\
        filter(measmt.date >= start).\
        filter(measmt.date <= end).all()

    session.close()

    tobs_list = []

    for min,avg,max in tobs_query:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)
   
if __name__ == "__main__":
    app.run(debug=True)