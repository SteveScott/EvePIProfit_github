import os, flask, sqlalchemy
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import urlparse

url = urlparse.urlparse(os.environ["DATABASE_URL"])

con = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)


os.environ['DATABASE_URL']='postgres://lojyjajvpwaaci:4ya_0u6olTZ2taL68me6Goa1HD@ec2-54-243-199-161.compute-1.amazonaws.com:5432/deaek2i6u7a13g'
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', table = "Table goes here")

@app.route('/jita')
def jita():
	return render_template('jita.html')

@app.route('/amarr')
def amarr():
	return render_template('amarr.html')

@app.route('/rens')
def rens():
	return render_template('rens.html')

#@app.route('/oursulaert')
#def oursulaert():
#	return render_template('oursulaert.html')

@app.route('/dodixie')
def dodixie():
	return render_template('dodixie.html')

if __name__ == "__main__":
    app.run(debug=True)
    app.run(debug=True)