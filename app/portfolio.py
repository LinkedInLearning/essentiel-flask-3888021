from flask import Flask, render_template, redirect, url_for
from app.modeles import projets, avis

app = Flask(__name__)


@app.errorhandler(404)
@app.route("/oups")
def introuvable(e=None):
    return render_template('introuvable.html')


@app.route("/")
def index():
    return render_template('index.html', liste=projets)


@app.route("/projet/<int:idproj>")
def projet(idproj):
    projet = next((p for p in projets if p['id'] == idproj), None)
    if projet is None:
        return redirect(url_for('introuvable'))
    return render_template('projet.html', projet=projet, avis=avis)
