import atexit
import os
import sys
#sys.path.insert(0, "~/Dropbox/1programming2/EVE/EvePIProfit_github/scripts")
import time
import requests
import urllib

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import logging
import json


import psycopg2 #You shouldn't be using psycopg2. Use SqlAlchemy

from flask import Flask, render_template, request, flash
from forms import ContactForm
from flask_wtf import Form
from flask_mail import Message, Mail
from scripts import eveLists
from scripts import connection
#from scripts import updatePrices
#from scripts import calculateMargins
#from scripts import PushToPerm
from scripts import connection
from scripts import eveLists
import atexit

from flask_sqlalchemy import SQLAlchemy

###scheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

logging.basicConfig(level=10)

current_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            "")
sys.path.append(current_path)


###end scheduler



#url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
'''
con = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
'''
mail = Mail()

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'evepiprofits@gmail.com'
app.config['MAILGUN_API_KEY'] = os.environ["MAILGUN_API_KEY"]
app.config['MAILGUN_DOMAIN'] = os.environ["MAILGUN_DOMAIN"]
app.config['TEMPLATES_AUTO_RELOAD'] = True

db = SQLAlchemy(app)



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
    #return render_template('maintenance.html')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/jita', methods=['GET', 'POST'])
def jita():
    #return render_template('maintenance.html')
    con = connection.establish_connection()
    cur = con.cursor()
    #cur.execute("SELECT * FROM temp_jita")
    cur.execute("SELECT name, price, profit, ROUND(profitmargin), mytime, cost, p_level FROM name, temp_jita WHERE itemid = id;")
    entries = cur.fetchall()
   # tax = 0 #request.form['tax_rate']

   # cur.execute('SELECT itemid, ROUND(profitmargin), mytime FROM perm_jita;')
   # persistentData = cur.fetchall()

   # chart = []

   # for entry in persistentData:
   #     chart.append({
   #         "itemid": entry[0],
   #         "profitmargin": entry[1],
   #         "mytime": str(entry[2])
   #     })
    cur.close()
    con.close()
    return render_template('jita.html', entries=entries)
   # if request.method == 'GET':
   #     return render_template('jita.html', entries=entries, chart=json.dumps(chart))
   # if request.method == 'POST':
   #     return render_template('jita.html', entries=entries, chart=json.dumps(chart))

@app.route('/amarr')
def amarr():
    #return render_template('maintenance.html')
    con = connection.establish_connection()
    cur = con.cursor()
    cur.execute("SELECT name, price, profit, ROUND(profitmargin), mytime, cost, p_level FROM name, temp_amarr WHERE itemid = id;")
    entries = cur.fetchall()
    cur.close()
    con.close()
    return render_template('amarr.html',entries=entries)


@app.route('/rens')
def rens():
   # return render_template('maintenance.html')
    con = connection.establish_connection()
    cur = con.cursor()
    cur.execute("SELECT name, price, profit, ROUND(profitmargin), mytime, cost, p_level FROM name, temp_rens WHERE itemid = id;")
    entries = cur.fetchall()
    cur.close()
    con.close()
    return render_template('rens.html',entries=entries)


#@app.route('/oursulaert')
#def oursulaert():
#	return render_template('oursulaert.html')

@app.route('/dodixie')
def dodixie():
   # return render_template('maintenance.html')
    con = connection.establish_connection()
    cur = con.cursor()
    cur.execute("SELECT name, price, profit, ROUND(profitmargin), mytime, cost, p_level FROM name, temp_dodixie WHERE itemid = id;")
    entries = cur.fetchall()
    cur.close()
    con.close()
    return render_template('dodixie.html',entries=entries)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    def send_mail(to_address, from_address, subject, plaintext):


        request = requests.post("https://api.mailgun.net/v3/%s/messages" % app.config['MAILGUN_DOMAIN'],
             auth=("api", app.config['MAILGUN_API_KEY']),
             data={
                 "from": from_address,
                 "to": to_address,
                 "subject": subject,
                 "text": plaintext,
                }
             )
        return request



    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('contact.html', form=form)
        else:
            try:
                send_mail(app.config["MAIL_USERNAME"],
                          form.email.data,
                          form.subject.data,
                          form.message.data)

                send_mail(form.email.data,
                          "no-reply@" + app.config["MAILGUN_DOMAIN"],
                          "Message sent to EVE PI Profits",
                          "Your message has been received, and we will get back to you promptly.")

                return render_template('posted.html')
            except requests.exceptions.RequestException as e:
                flash(e)




    elif request.method == 'GET':
        return render_template('contact.html', form=form)


if __name__ == "__main__":
    print('launching app.run')
    app.run(debug=True, port=os.environ.get('PORT', 5000), use_reloader=True)
    #app.run(debug=True)

