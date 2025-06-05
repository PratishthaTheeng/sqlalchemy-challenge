# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy

from flask import Flask, jsonify,Blueprint
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from utils import convert_date_to_str,get_year_ago
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.prepare(autoload_with=engine)

# Save references to each table
Measurement = base.classes.measurement
Station = base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1.0')

#################################################
# Flask Routes
#################################################
@api_v1.route('/precipitation')
def get_precipitation():
    recent= session.query(
        Measurement.date
    ).order_by(
        Measurement.date.desc()
    ).first()

    recent_data_point = convert_date_to_str(recent.date)
    year_data = get_year_ago(recent_data_point)
    data = session.query(
            Measurement.date, Measurement.prcp
        ).filter(
            sqlalchemy.and_(
                Measurement.date >= year_data,
                Measurement.prcp >= 0
            )
        ).all()
    
    response = {item.date: item.prcp for item in data}
    return jsonify(response)
    
@api_v1.route("/stations")
def get_stations():
    stations = session.query(
                Station.station,
                Station.name
            ).all()
    response = {station.station: station.name for station in stations}
    return jsonify(response)
    
@api_v1.route("/tobs")
def get_tobs():
    most_active_stations = session.query(
        Measurement.station, 
        func.count(Measurement.prcp).label('count')
    ).group_by(
        Measurement.station
    ).order_by(
        func.count(Measurement.prcp).desc()
    )
    recent= session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    active_station = most_active_stations.first()
    recent_data_point = convert_date_to_str(recent.date)

    year_data = get_year_ago(recent_data_point)
    result = session.query(
            Measurement.date, Measurement.tobs
        ).filter(
            sqlalchemy.and_(
                Measurement.date >= year_data,
                Measurement.station == active_station.station
            )
        ).all()
    response = {item.date: item.tobs for item in result}
    return jsonify(response)

@api_v1.route("/<start>")
def get_data_by_start_point(start):
    start_date = convert_date_to_str(start)
    result = session.query(
            func.min(Measurement.tobs).label("min_tobs"),
            func.max(Measurement.tobs).label('max_tobs'),
            func.avg(Measurement.tobs).label("avg_tobs")
        ).filter(
            Measurement.date >= start_date
        ).first()
    
    return jsonify({
        'min_tobs':result.min_tobs,
        'max_tobs': result.max_tobs,
        'avg_tobs': result.avg_tobs
    })
    
@api_v1.route("/<start>/<end>")
def get_data_by_start_end_point(start,end):
    start_date = convert_date_to_str(start)
    end_date = convert_date_to_str(end)
    
    result = session.query(
            func.min(Measurement.tobs).label("min_tobs"),
            func.max(Measurement.tobs).label('max_tobs'),
            func.avg(Measurement.tobs).label("avg_tobs")
        ).filter(
            sqlalchemy.and_(
                Measurement.date >= start_date,
                Measurement.date <= end_date
            )
        ).first()
       
    return jsonify({
        'min_tobs':result.min_tobs,
        'max_tobs': result.max_tobs,
        'avg_tobs': result.avg_tobs
    })
    
    
@api_v1.route("/")
def home():
    return jsonify(
        {
            "message": "climate app api version 1"
        }
    )    
    
app.register_blueprint(api_v1)

if __name__ == "__main__":
    app.run(debug=True)