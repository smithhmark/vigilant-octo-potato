import sqlite3 
import os

import geonames

def get_connection():
    dbpath = os.environ.get("DBPATH", "./data/geo.db")
    return sqlite3.connect(dbpath)

def build_schema(conn):
    sql = """create table if not exists kidgeo
    ( geonameid INTEGER PRIMARY KEY,
    name TEXT,
    latitude REAL,
    longitude REAL);"""
    conn.execute(sql)

def insert_kidrecord(curs, record):
    id = record['geonameid']
    name = record['name']
    lat = float(record['latitude'])
    lon = float(record['longitude'])

    sql = """insert into kidgeo (geonameid, name, latitude, longitude)
    values
    (?,?,?,?)""" 
    curs.execute(sql, (id, name, lat, lon))

def load_simple(conn, records, commit=True):
    curs = conn.cursor()
    for rec in records:
        insert_kidrecord(curs, rec)
    if commit:
        conn.commit()

def find_by_name(conn, name):
    sql = """select * from kidgeo
    where name=?"""
    cc = conn.cursor()
    cc.execute(sql, (name,))
    rows = cc.fetchall()
    return rows

def find_by_name_fragment(conn, name):
    sql = """select * from kidgeo
    where name like ?"""
    cc = conn.cursor()
    tmp = "%{}%".format(name)
    cc.execute(sql, (tmp,))
    rows = cc.fetchall()
    return rows

def find_by_location(conn, lat, lon):
    sql = """select * from kidgeo
    where latitude=? and longitude=?"""
    cc = conn.cursor()
    cc.execute(sql, (lat,lon))
    rows = cc.fetchall()
    return rows

def find_by_id(conn, geoid):
    sql = """select * from kidgeo
    where geonameid=?"""
    cc = conn.cursor()
    cc.execute(sql, (geoid,))
    rows = cc.fetchall()
    return rows

def get_spatial_records(conn):
    sql = """select geonameid, latitude, longitude
    from kidgeo"""
    results = []
    cc = conn.cursor()
    cc.execute(sql)
    rows = cc.fetchall()
    for row in rows:
        results.append({"geonameid": int(row[0]),
            "latitude": row[1],
            "longitude": row[2], })
    return results
