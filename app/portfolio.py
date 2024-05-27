from flask import Flask, render_template
from app.modeles import projets, avis

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html', liste=projets)


@app.route("/projet")
def projet():
    return render_template('projet.html', projet=projets[1], avis=avis)
