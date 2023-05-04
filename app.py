# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import func
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func,inspect
import datetime as dt

#################################################
# Database Setup
#################################################
# reflect an existing database into a new model
# reflect the tables
# Save references to each table
# Create our session (link) from Python to the DB
from sqlalchemy import create_engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

#################################################
# Flask Setup
#################################################




#################################################
# Flask Routes
#################################################



# set up database and create Flask app


# define routes
@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return precipitation data for the last year."""
    # Calculate the date 1 year ago from today
    last_year = dt.date.today() - dt.timedelta(days=365)

    # Query the database for precipitation data
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= last_year).all()

    # Convert the query results to a dictionary with date as the key and prcp as the value
    precip_dict = {}
    for result in results:
        date = result[0]
        prcp = result[1]
        precip_dict[date] = prcp

    # Return the JSON representation of the dictionary
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations."""
    # Query the database for station data
    results = session.query(Station.station, Station.name).all()

    # Convert the query results to a list of dictionaries
    stations_list = []
    for result in results:
        station = result[0]
        name = result[1]
        stations_list.append({"station": station, "name": name})

    # Return the JSON representation of the list
    return jsonify(stations_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature(start, end=None):
    """Return the minimum, average, and maximum temperatures for a given date range."""
    # Convert the date string to a datetime object
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")

    # Calculate the end date if it was provided
    if end:
        end_date = dt.datetime.strptime(end, "%Y-%m-%d")
    else:
        end_date = dt.date.today()

    # Query the database for temperature data
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    # Convert the query results to a list of dictionaries
    temps_list = []
    for result in results:
        min_temp = result[0]
        avg_temp = result[1]
        max_temp = result[2]
        temps_list.append({"Min Temp": min_temp, "Avg Temp": avg_temp, "Max Temp": max_temp})

    # Return the JSON representation of the list
    return jsonify(temps_list)

# run the app
if __name__ == '__main__':
    app.run()
