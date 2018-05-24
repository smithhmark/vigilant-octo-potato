import sqlite3 

import geonames

def get_connection():
    return sqlite3.connect("./data/geo.db")

def build_schema(conn):
    sql = """create table if not exists kidgeo
    ( id INTEGER PRIMARY KEY,
    name TEXT,
    latitude REAL,
    longitude REAL);"""
    conn.execute(sql)

def insert_kidrecord(curs, record):
    id = record['id']
    name = record['name']
    lat = float(record['latitude'])
    lon = float(record['longitude'])

    sql = """insert into kidgeo (id, name, latitude, longitude)
    values
    (?,?,?,?)""" 
    curs.execute(sql, (id, name, lat, lon))

def load_simple(conn, records):
    curs = conn.cursor()
    for rec in records:
        insert_kidrecord(curs, rec)

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
    where id=?"""
    cc = conn.cursor()
    cc.execute(sql, (geoid,))
    rows = cc.fetchall()
    return rows
