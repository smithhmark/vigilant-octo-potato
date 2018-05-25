
from flask import Flask
from flask import request
from flask import abort

app = Flask(__name__)

import db
import spatial
import responses

def _setup():
    conn = db.get_connection()
    recs = db.get_spatial_records(conn)
    return spatial.Spatial(recs)
SPATIAL = _setup()

@app.route('/')
def home():
    return responses.index_page()

@app.route('/cities/<geonameid>/nearest/<k>')
def neighbor_cities(geonameid, k):
    gid = int(geonameid)
    loc = SPATIAL.loc_at_id(gid)
    kk = int(k)
    res = SPATIAL.knn(kk, loc)
    return responses.distances_page(res)

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
            return "I don't understand the request", 400
        return responses.city_list_page(
                [db.make_city_dict(cc) for cc in results])
    else:
        return "not yet implemented", 400

@app.route('/cities/<geonameid>')
def cities(geonameid):
    conn = db.get_connection()
    gid = int(geonameid)
    results = db.find_by_id(conn, gid)
    if len(results) == 1:
        return responses.city_desc_page(db.make_city_dict(results[0]))
    else:
        abort(404)
