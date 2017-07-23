import sqlite3
import csv
from pprint import pprint
from time import time


#time at start of running code
t0 = time()

sqlite_file = 'mydb.db'    # name of the sqlite database file

# Connect to the database
conn = sqlite3.connect(sqlite_file)
# Get a cursor object
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS nodes')
conn.commit()

#The following code below creates a database from the excel files 

# Create the table, specifying the column names and data types:
cur.execute('''
    CREATE TABLE IF NOT EXISTS nodes_tags(id INTEGER, key TEXT, value TEXT,type TEXT)
''')
# commit the changes
conn.commit()

# Read in the csv file as a dictionary, format the
# data as a list of tuples:

with open('nodes_tags.csv','rb') as fin:
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['id'], i['key'].decode("utf-8"),i['value'].decode("utf-8"), i['type']) for i in dr]
# insert the formatted data
cur.executemany("INSERT INTO nodes_tags(id, key, value,type) VALUES (?, ?, ?, ?);", to_db)
# commit the changes
conn.commit()

# Create the table, specifying the column names and data types:
cur.execute('''
    CREATE TABLE nodes(id INTEGER, lat INTEGER, lon INTEGER, user TEXT, uid TEXT, version INTEGER, changeset INTEGER,timestamp TEXT)
''')
# commit the changes
conn.commit()

#time elapsed at this point of the code
print 'Time elapsed: {} seconds'.format(round(time()-t0,2))

# Read in the csv file as a dictionary, format the
# data as a list of tuples:

with open('nodes.csv','rb') as fin:
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['id'].decode("utf-8"), i['lat'].decode("utf-8"), i['lon'].decode("utf-8"),
              i['user'].decode("utf-8"), i['uid'].decode("utf-8"), i['version'].decode("utf-8"),
              i['changeset'].decode("utf-8"), i['timestamp'].decode("utf-8")) for i in dr]
# insert the formatted data
cur.executemany("INSERT INTO nodes(id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
# commit the changes
conn.commit()

# Create the table, specifying the column names and data types:
cur.execute('''
    CREATE TABLE ways(id INTEGER, user TEXT, uid INTEGER, version INTEGER, changeset INTEGER, timestamp TEXT)
''')
# commit the changes
conn.commit()

# Read in the csv file as a dictionary, format the
# data as a list of tuples:

with open('ways.csv','rb') as fin:
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['id'].decode("utf-8"), i['user'].decode("utf-8"), i['uid'].decode("utf-8"), i['version'].decode("utf-8"), i['changeset'].decode("utf-8"), i['timestamp'].decode("utf-8")) for i in dr]
# insert the formatted data
cur.executemany("INSERT INTO ways(id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);", to_db)
# commit the changes
conn.commit()

# Create the table, specifying the column names and data types:
cur.execute('''
    CREATE TABLE ways_nodes(id INTEGER, node_id INTEGER, position INTEGER)
''')
# commit the changes
conn.commit()

# Read in the csv file as a dictionary, format the
# data as a list of tuples:

with open('ways_nodes.csv','rb') as fin:
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['id'], i['node_id'],i['position']) for i in dr]
# insert the formatted data
cur.executemany("INSERT INTO ways_nodes(id, node_id, position) VALUES (?, ?, ?);", to_db)
# commit the changes
conn.commit()

# Create the table, specifying the column names and data types:
cur.execute('''
    CREATE TABLE ways_tags(id INTEGER, key TEXT, value TEXT,type TEXT)
''')
# commit the changes
conn.commit()


with open('ways_tags.csv','rb') as fin:
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['id'], i['key'],i['value'].decode("utf-8"), i['type']) for i in dr]
# insert the formatted data
cur.executemany("INSERT INTO ways_tags(id, key, value,type) VALUES (?, ?, ?, ?);", to_db)
# commit the changes
conn.commit()

#total time took to run code
print 'Time Executed: {} seconds'. format(round(time()-t0,2))

conn.close()
