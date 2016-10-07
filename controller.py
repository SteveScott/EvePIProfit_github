from flask import Flask, render_template, url_for
app = Flask(__name__)

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

@app.route('/oursulaert')
def oursulaert():
	return render_template('oursulaert.html')

@app.route('/dodixie')
def dodixie():
	return render_template('dodixie.html')

if __name__ == "__main__":
    app.run(debug=True)
    app.run(debug=True)