from flask import Flask, render_template, redirect, url_for, request
from app.modeles import Projet, Avis, Contact, db
from app.forms import FormAvis
from os import path

app = Flask(__name__, 
            instance_path=path.abspath('instance'), 
            instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
db.init_app(app)


@app.errorhandler(404)
@app.route("/oups")
def introuvable(e=None):
    return render_template('introuvable.html')


@app.route("/")
def index():
    projets = db.session.query(Projet).all()
    return render_template('index.html', liste=projets)


@app.route("/projet/<int:idproj>")
def projet(idproj):
    form = None
    if 'formavis' in request.values:
        form = FormAvis()
    if 'idavis' in request.args:
        idavis = request.args.get('idavis')
        avis = db.get_or_404(Avis, idavis)
        avis.likes += 1
        db.session.commit()
        return redirect(url_for('projet', idproj=idproj, _anchor='liste-avis'))
    projet = db.get_or_404(Projet, idproj)
    return render_template('projet.html', projet=projet, formavis=form)


@app.route("/admin")
def admin():
    return render_template(
        'admin.html', 
        avis = db.session
            .query(Avis)
            .filter_by(ok=False), # .where(Avis.ok == False)
        contacts = db.session
            .query(Contact)
            .order_by(Contact.creation.desc())
            .limit(20),
        utilisateurs = []
    )


@app.route("/admin/avis/<int:idavis>/ok")
def admin_avis_ok(idavis):
    avis = db.get_or_404(Avis, idavis)
    avis.ok = True
    db.session.commit()
    return redirect(url_for('admin', _anchor='moderation'))

@app.route("/admin/avis/<int:idavis>/suppr")
def admin_avis_suppr(idavis):
    avis = db.get_or_404(Avis, idavis)
    db.session.delete(avis)
    db.session.commit()
    return redirect(url_for('admin', _anchor='moderation'))

@app.route("/admin/contact/<int:idcontact>/suppr")
def admin_contact_suppr(idcontact):
    contact = db.get_or_404(Contact, idcontact)
    db.session.delete(contact)
    db.session.commit()
    return redirect(url_for('admin', _anchor='contacts'))
