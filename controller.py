import atexit
import os
import time
import urllib
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import sys
import logging
import json
from gitIgnore import passwords

import psycopg2

from flask import Flask, render_template, request, flash
from forms import ContactForm
from flask_mail import Message, Mail
from scripts import updatePrices
from scripts import calculateMargins
from scripts import PushToPerm

###scheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

logging.basicConfig(level=10)





###end scheduler

os.environ['DATABASE_URL']='postgres://lojyjajvpwaaci:4ya_0u6olTZ2taL68me6Goa1HD@ec2-54-243-199-161.compute-1.amazonaws.com:5432/deaek2i6u7a13g'

url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

con = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

mail = Mail()

app = Flask(__name__)
app.secret_key = 'qDB5kyrKD8YlscV2JrbKSkdJfndzMgTxN '
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'evepiprofit@gmail.com'
app.config["MAIL_PASSWORD"] = passwords.email()
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

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('contact.html', form=form)
        else:
            msg = Message(form.subject.data, sender='evepiprofits@gmail.com', recipients=['stevescott517@gmail.com', 'evepiprofits@gmail.com'])
            msg.body ="""
            From %s <%s>
            %s
            """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)

            return render_template('posted.html')
    elif request.method == 'GET':
        return render_template('contact.html', form = form)


if __name__ == "__main__":
    print('launching app.run')
    app.run(debug=True, port=os.environ.get('PORT', 5000), use_reloader=False)
    #app.run(debug=True)