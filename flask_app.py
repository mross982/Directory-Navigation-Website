from app import app, db
from app.models import User, Container, Category, Link


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Container': Container, 'Category': Category, 'Link': Link}













from flask import Flask, render_template, url_for
from assets import css
from flask_assets import Bundle, Environment
from mikelinks import MLinks
from kevinlinks import KLinks
import webbrowser



app = Flask(__name__)
print(type(app))
assets = Environment(app)
assets.register('css', css)

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/michael", methods =['GET', 'POST'])
def michael():
    return render_template('michael.html', mikelinks=MLinks)


@app.route("/kevin")
def kevinw():
    return render_template('kevin.html', kevinlinks=KLinks)

@app.route("/lydia")
def lydia():
    return "Hey Lydia"

@app.route("/tbd")
def tbd():
    return "Hey New Person"

@app.route("/dsrip")
def dsrip():
    return render_template('dsrip.html')

# @app.route("/members/<name>/")
# def getMember(name):
#     return name
webbrowser.open("localhost")

if __name__ == "__main__":
    app.run(debug=False, port=80)
    # The port=80 argument gets rid of the need to put 5000 after localhost in the browser.
