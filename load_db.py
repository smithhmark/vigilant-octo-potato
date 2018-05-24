import os
import zipfile
import sys

import db
import geonames

if __name__ == '__main__':
    conn = db.get_connection()

    db.build_schema(conn)

    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = "./data/cities1000.zip"

    with zipfile.ZipFile(filepath) as myzip:
        if 'cities1000.txt' not in myzip.namelist():
            print("failed to find cities1000 data at indicated location")
            os.exit(1)

        with myzip.open('cities1000.txt', 'r') as myfile:
            data = geonames.read_bfile_raw(myfile)
            db.load_simple(conn, data)

