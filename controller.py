import atexit
import os
import time
import urlparse
import sys
import logging
import json

import psycopg2

from flask import Flask, render_template
from scripts import updatePrices
from scripts import calculateMargins
from scripts import PushToPerm
###scheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

logging.basicConfig(level=10)





###end scheduler

os.environ['DATABASE_URL']='postgres://lojyjajvpwaaci:4ya_0u6olTZ2taL68me6Goa1HD@ec2-54-243-199-161.compute-1.amazonaws.com:5432/deaek2i6u7a13g'

url = urlparse.urlparse(os.environ["DATABASE_URL"])

con = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)


app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/jita')
def jita():
    cur = con.cursor()
    #cur.execute("SELECT * FROM temp_jita")
    cur.execute("SELECT name, price, profit, ROUND(profitmargin), mytime FROM name, temp_jita WHERE itemid = id;")
    entries = cur.fetchall()
    cur.execute('SELECT itemid, ROUND(profitmargin), mytime FROM perm_jita;')
    persistentData = cur.fetchall()

    chart = []

    for entry in persistentData:
        chart.append({
            "itemid": entry[0],
            "profitmargin": entry[1],
            "mytime": str(entry[2])
        })

    return render_template('jita.html',entries=entries, chart=json.dumps(chart))

@app.route('/amarr')
def amarr():
    cur = con.cursor()
    cur.execute("SELECT name, price, profit, ROUND(profitmargin), mytime FROM name, temp_amarr WHERE itemid = id;")
    entries = cur.fetchall()
    return render_template('amarr.html',entries=entries)

@app.route('/rens')
def rens():
    cur = con.cursor()
    cur.execute("SELECT name, price, profit, ROUND(profitmargin), mytime FROM name, temp_rens WHERE itemid = id;")
    entries = cur.fetchall()
    return render_template('rens.html',entries=entries)


#@app.route('/oursulaert')
#def oursulaert():
#	return render_template('oursulaert.html')

@app.route('/dodixie')
def dodixie():
    cur = con.cursor()
    cur.execute("SELECT name, price, profit, ROUND(profitmargin), mytime FROM name, temp_dodixie WHERE itemid = id;")
    entries = cur.fetchall()
    return render_template('dodixie.html',entries=entries)


if __name__ == "__main__":
    print('launching app.run')
    app.run(debug=True, port=os.environ.get('PORT', 5000), use_reloader=False)
    #app.run(debug=True)