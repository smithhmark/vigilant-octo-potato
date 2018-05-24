
from flask import Flask
from flask import request

app = Flask(__name__)

import db
import spatial

def _setup():
    conn = db.get_connection()
    recs = db.get_spatial_records(conn)
    return spatial.Spatial(recs)
SPATIAL = _setup()

@app.route('/')
def home():
    return "really?"

@app.route('/cities/<geonameid>/nearest/<k>')
def neighbor_cities(geonameid, k):
    gid = int(geonameid)
    loc = SPATIAL.loc_at_id(gid)
    kk = int(k)
    res = SPATIAL.knn(kk, loc)
    return repr(res)

@app.route('/cities')
def find_cites():
    conn = db.get_connection()
    if len(request.args) > 0:
        if "partial_name" in request.args:
            term = request.args['partial_name']
            results = db.find_by_name_fragment(conn, term)
        elif "name" in request.args:
            term = request.args['name']
            results = db.find_by_name(conn, term)
        else:
            return ""
        return repr(results)
    else:
        return "not yet implemented"

@app.route('/cities/<geonameid>')
def cities(geonameid):
    conn = db.get_connection()
    gid = int(geonameid)
    results = db.find_by_id(conn, gid)
    if len(results) == 1:
        return repr(results[0])
    else:
        return "cities, {}".format(geonameid)
