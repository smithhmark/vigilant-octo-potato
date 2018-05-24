import pytest
import pandas as pd
import math

import spatial

@pytest.fixture()
def test_data_simple():
    return [
            {"x": 0, "y":0, "z":0},
            {"x": 1, "y":0, "z":0},
            {"x": 0, "y":1, "z":0},
            {"x": 0, "y":0, "z":1},
            {"x": 1, "y":1, "z":1},
            {"x": 10, "y":10, "z":10},
            {"x": 11, "y":10, "z":10},
            {"x": 10, "y":11, "z":10},
            {"x": 10, "y":10, "z":110},
            ]

@pytest.fixture()
def test_data():
    labels = ["geonameid", "name", "latitude", "longitude"]
    tmp = [
            [5391959, "San Francisco", 37.77493, -122.41942],
            [5397765, "South San Francisco", 37.65466, -122.40775],
            [5378538, "Oakland", 37.80437, -122.2708],
            [5392567, "San Rafael", 37.97353, -122.53109],
            ]
    final = []
    for ii in tmp:
        final.append(dict(zip(labels, ii)))
    return final

def test_lat_long_rad_to_XYZ():
    x,y,z = spatial.lat_long_rad_to_XYZ(0, 0, 0)
    assert x == 0
    assert y == 0
    assert z == 0

    x,y,z = spatial.lat_long_rad_to_XYZ(0, 0, 1)
    assert x == 1
    assert y == 0
    assert z == 0


def test_mappings():
    fake_recs = [{"geonameid": ii} for ii in range(100,110)]

    toid, tooffset = spatial.id_offset_mappings(fake_recs)
    for ii in range(10):
        assert ii in toid
        assert toid[ii] == 100 + ii

    for ii in range(100, 110):
        assert ii in tooffset
        assert tooffset[ii] == ii - 100

def test_mappings(test_data):
    toid, tooffset = spatial.id_offset_mappings(test_data)
    assert tooffset[5391959] == 0
    assert toid[0] == 5391959

    assert tooffset[5378538] == 2
    assert toid[2] == 5378538

def _dist_latlon(i1, i2):
    c1 = spatial.lat_long_record_to_XYZ(i1)
    c2 = spatial.lat_long_record_to_XYZ(i2)
    print(i1,i2)
    return _dist_xyz(c1, c2)

def _dist_xyz(c1, c2):
    dx = c2['x'] - c1['x']
    dy = c2['y'] - c1['y']
    dz = c2['z'] - c1['z']
    print(c1,c2)
    return math.sqrt(dx*dx + dy*dy * dz*dz)

def test_Spatial(test_data):
    testee = spatial.Spatial(test_data)
    gdata = [spatial.lat_long_record_to_XYZ(ii) for ii in test_data]

    assert testee is not None
    #print(testee.loc_at_idx(0))
    #print(testee._df)
    coords = pd.Series(gdata[0])
    assert testee.loc_at_idx(0).equals(coords)

    results = testee.knn(2, coords)
    #print(results)
    assert len(results) == 2
    assert results[0]["dist"] == 0
    assert results[0]["geonameid"] == test_data[0]['geonameid']
    assert results[1]["geonameid"] == test_data[1]['geonameid']
    assert results[1]["dist"] < 15
    assert results[1]["dist"] > 10
    #_dist_latlon(test_data[0], test_data[1])

    results = testee.knn(3, coords)
    #print(results)
    assert len(results) == 3
    assert results[0]["dist"] == 0
    assert results[0]["geonameid"] == test_data[0]['geonameid']
    assert results[1]["geonameid"] == test_data[1]['geonameid']
    assert results[1]["dist"] < 14
    assert results[1]["dist"] > 13
    assert results[2]["geonameid"] == test_data[2]['geonameid']
    assert results[2]["dist"] < 14
    assert results[2]["dist"] > 13
