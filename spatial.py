import scipy.spatial as scpsp
import math
import pandas as pd

import geonames

class Spatial:
    def __init__(self, raw_data):
        self._df = geo_data_from_records(raw_data)
        self._tree = scpsp.KDTree(self._df)
        self._offset_to_id, self._id_to_offset = id_offset_mappings(raw_data)

    def loc_at_idx(self, idx):
        return self._df.iloc[idx]

    def loc_at_id(self, geoid):
        offset = self._id_to_offset[geoid]
        return self.loc_at_idx(offset)

    def knn(self, k, coq):
        dists, neighbors = self._tree.query(coq, k)
        res = []
        for ii, nn in enumerate(neighbors):
            res.append({"dist": dists[ii], "id": self._offset_to_id[nn]})
        return res

AVG_EARTH_RADIUS = 6.3781 * math.pow(10,3) # in km

def lat_long_record_to_XYZ(record):
    """take a dict record with lat and long and return the 3-space equiv
    currently using spherical approximation for Earth
    """
    lat = record['latitude']
    lon = record['longitude']
    x,y,z = lat_long_rad_to_XYZ(lat, lon, AVG_EARTH_RADIUS)
    return {"x":x, "y": y, "z": z}

def lat_long_rad_to_XYZ(lat, lon, radius):
    """
    x = R * cos(lat) * cos(lon)
    y = R * cos(lat) * sin(lon)
    z = R *sin(lat)
    """
    x = radius * math.cos(math.radians(lat)) * math.cos(math.radians(lon))
    y = radius * math.cos(math.radians(lat)) * math.sin(math.radians(lon))
    z = radius *math.sin(math.radians(lat))
    return x,y,z

def id_offset_mappings(records):
    toid = {}
    tooffset = {}
    for ii, rr in enumerate(records):
        toid[ii] = rr["id"]
        tooffset[rr["id"]] = ii
    return toid, tooffset

def geo_data_from_records(records):
    tmp = geonames.slice_geo_data(records)
    spatial_recs = [lat_long_record_to_XYZ(rec) for rec in tmp]
    return pd.DataFrame(spatial_recs)
