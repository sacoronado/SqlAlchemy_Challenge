import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Database Setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")


Base = automap_base()

Base.prepare(engine, reflect=True)


measurement = Base.classes.measurement
station = Base.classes.station


# Flask Setup

app = Flask(__name__)



# Home Page and Flask Routes


@app.route("/")
def home():
    return (
        f"Hey there..<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date [Format: yyyy-mm-dd] <br/>"
        f"/api/v1.0/start_date/end_date [Format: yyyy-mm-dd]"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)

    
    
    results = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date > '2016-08-23').\
    order_by(measurement.date).all()

    session.close()

    
    precipitation = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        precipitation.append(prcp_dict)

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)


    s_results = session.query(station.station).all()
  
    session.close()

    all_stations = list(np.ravel(s_results))
    
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    tmp_df = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date > '2016-08-23').\
    filter(measurement.station == 'USC00519281').\
    order_by(measurement.date).all()

    session.close()

    
    all_temps = list(np.ravel(tmp_df))

    return jsonify(all_tmps)


@app.route("/api/v1.0/<start_date>")
def start_date(start_date):
    session = Session(engine)

   
    sel = [measurement.tobs, 
       func.min(measurement.tobs), 
       func.avg(measurement.tobs), 
       func.max(measurement.tobs)]
    
    tmp_stats = session.query(*sel).\
        filter(measurement.date >= start_date).all()

    session.close()


    tmp = list(np.ravel(tmp_stats))

    return jsonify(tmps)



@app.route("/api/v1.0/<start_date>/<end_date>")
def date_range(start_date, end_date):
    
    session = Session(engine)

    sel = [measurement.tobs, 
       func.min(measurement.tobs), 
       func.avg(measurement.tobs), 
       func.max(measurement.tobs)]
    
    tmp_stats = session.query(*sel).\
        filter(measurement.date >= start_date).\
        filter(measurement.date <= end_date).all()

    session.close()


    dtemps = list(np.ravel(tmp_stats))

    return jsonify(dtemps)


if __name__ == "__main__":
    app.run(debug=True)