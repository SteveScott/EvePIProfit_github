from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', table = "Table goes here")

if __name__ == "__main__":
    app.run(debug=True)
    app.run(debug=True)