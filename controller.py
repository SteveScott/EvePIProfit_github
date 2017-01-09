import atexit
import os
import time
import urlparse
import sys

import psycopg2

from flask import Flask, render_template
from scripts import updatePrices
from scripts import calculateMargins
###scheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

def print_date_time():
    print('Updating Tables')
    updatePrices.main()
    #execfile(scripts/updatePrices.py)
    print('Updating Margins')
    calculateMargins.main()
    #execfile(scripts/calculateMargins.py)
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=print_date_time, # your function here
    trigger=IntervalTrigger(minutes=360),
    id='doingsmth_job',
    name='Update tables and recalculate profit margins every 6 hours',
    replace_existing=True)

atexit.register(lambda: scheduler.shutdown())

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
    return render_template('index.html', table = "Table goes here")

@app.route('/jita')
def jita():
    cur = con.cursor()
    #cur.execute("SELECT * FROM temp_jita")
    cur.execute("SELECT name, price, profit, ROUND(profitmargin), mytime FROM name, temp_jita WHERE itemid = id")
    entries = cur.fetchall()
    return render_template('jita.html',entries=entries)

@app.route('/amarr')
def amarr():
    cur = con.cursor()
    cur.execute("SELECT name, price, profit, ROUND(profitmargin), mytime FROM name, temp_amarr WHERE itemid = id")
    entries = cur.fetchall()
    return render_template('amarr.html',entries=entries)

@app.route('/rens')
def rens():
    cur = con.cursor()
    cur.execute("SELECT name, price, profit, ROUND(profitmargin), mytime FROM name, temp_rens WHERE itemid = id")
    entries = cur.fetchall()
    return render_template('rens.html',entries=entries)


#@app.route('/oursulaert')
#def oursulaert():
#	return render_template('oursulaert.html')

@app.route('/dodixie')
def dodixie():
    cur = con.cursor()
    cur.execute("SELECT name, price, profit, ROUND(profitmargin), mytime FROM name, temp_dodixie WHERE itemid = id")
    entries = cur.fetchall()
    return render_template('dodixie.html',entries=entries)


if __name__ == "__main__":

    app.run(debug=True, port=os.environ.get('PORT', 5000))
    #app.run(debug=True)