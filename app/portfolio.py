from flask import Flask, render_template
from app.modeles import projets, avis

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html', liste=projets)


@app.route("/projet/<int:idproj>")
def projet(idproj):
    projet = next(p for p in projets if p['id'] == idproj)
    return render_template('projet.html', projet=projet, avis=avis)
