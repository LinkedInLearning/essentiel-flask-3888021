from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from app.modeles import Projet, Avis, db
from app.forms import FormAvis
from datetime import timedelta

bp = Blueprint('portfolio', __name__, url_prefix='/portfolio')


@bp.route("/")
def index():
    projets = db.session.query(Projet).all()
    return render_template('index.html', liste=projets)


@bp.route("/projet/<int:idproj>", methods=['GET', 'POST'])
def projet(idproj):
    form = None
    if 'formavis' in request.values:
        avis = Avis()
        avis.id_projet = idproj
        form = FormAvis(request.form, avis, meta={
            'csrf_context': session,
            'csrf_secret' : app.config['CSRF_SECRET'],
            'csrf_time_limit': timedelta(minutes=app.config['CSRF_MINUTES'])
        })
        if request.method == 'POST' and 'avis' in request.values and form.validate():
            form.populate_obj(avis)
            db.session.add(avis)
            db.session.commit()
            flash("Merci pour votre retour ! Votre avis apparaîtra dés sa validation.", 'success')
            return redirect(url_for('projet', idproj=idproj))
    if 'idavis' in request.args:
        idavis = request.args.get('idavis')
        avis = db.get_or_404(Avis, idavis)
        if 'likes' not in session:
            session['likes'] = []    
        if idavis in session['likes']:
            flash(f"Déjà fait ! Votre like pour l'avis de {avis.auteur} a déjà été pris en compte.", 'warning')
            return redirect(url_for('projet', idproj=idproj))
        session['likes'].append(idavis)
        avis.likes += 1
        flash(f"Et de {avis.likes} ! Votre like sur l'avis de {avis.auteur} est comptabilisé.", 'success')
        db.session.commit()
        return redirect(url_for('projet', idproj=idproj, _anchor='liste-avis'))
    projet = db.get_or_404(Projet, idproj)
    return render_template('projet.html', projet=projet, formavis=form)
