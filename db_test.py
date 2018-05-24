import sqlite3
import pytest

import db

@pytest.fixture()
def blankdb():
    return sqlite3.connect(":memory:")

@pytest.fixture()
def emptydb(blankdb):
    db.build_schema(blankdb)
    return blankdb

@pytest.fixture()
def example_record():
    return {"id": 1, 
            "name": "Oz",
            "latitude": 26.2,
            "longitude": 3.14159,
            }

@pytest.fixture()
def example_records(example_record):
    recs = [example_record]
    recs.append({"id": 2, 
            "name": "South Oz",
            "latitude": 16.2,
            "longitude": 3.14159,
            })
    recs.append({"id": 3, 
            "name": "West Oz",
            "latitude": 26.2,
            "longitude": 13.14159,
            })
    return recs

@pytest.fixture()
def populated_db(emptydb, example_records):
    db.load_simple(emptydb, example_records)
    return emptydb

def test_insert_kidrecord(emptydb, example_record):
    db.insert_kidrecord(emptydb, example_record)

    cc = emptydb.cursor()
    cc.execute("select * from kidgeo")
    rows = cc.fetchall()
    assert len(rows) == 1
    assert rows[0][0] == example_record['id']
    assert rows[0][1] == example_record['name']
    assert rows[0][2] == example_record['latitude']
    assert rows[0][3] == example_record['longitude']

def test_find_by_name(populated_db):
    rows = db.find_by_name(populated_db, "Oz")
    assert len(rows) == 1

    rows = db.find_by_name(populated_db, "Whisteria")
    assert len(rows) == 0

def test_find_by_name_frag(populated_db):
    rows = db.find_by_name_fragment(populated_db, "Oz")
    assert len(rows) == 3

    rows = db.find_by_name(populated_db, "Whisteria")
    assert len(rows) == 0

def test_find_by_location(populated_db):
    rows = db.find_by_location(populated_db, 26.2, 3.14159)
    assert len(rows) == 1

    rows = db.find_by_location(populated_db, 26.2, 30.14159)
    assert len(rows) == 0

def test_find_by_id(populated_db):
    rows = db.find_by_id(populated_db, 1)
    assert len(rows) == 1

    rows = db.find_by_id(populated_db, 14159)
    assert len(rows) == 0
