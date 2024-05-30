from flask import Blueprint, render_template, current_app, redirect, url_for, request, session, flash
from markupsafe import Markup
from app.modeles import Projet, Avis, Contact, db
from app.forms import FormAvis
from app.services import cache
from datetime import timedelta

bp = Blueprint('portfolio', __name__, url_prefix='/portfolio')


def contact(sujet):
    mail = Markup(request.values.get('mail')).striptags()
    message = Markup(request.values.get('message')).striptags()
    if not mail or not sujet or not message:
        flash("Problème ! Tous les champs du formulaire de contact sont obligatoires.", "alert")
        return False
    db.session.add(Contact(mail=mail, sujet=sujet, message=message))
    db.session.commit()
    flash("Merci ! Je vous recontacte rapidement.", "success")
    return True


@cache.cached()
@bp.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and contact(Markup(request.values.get('sujet')).striptags()):
        return redirect(url_for('portfolio.index'))
    projets = db.session.query(Projet).all()
    return render_template('portfolio/index.html', liste=projets)


@bp.route("/projet/<int:idproj>", methods=['GET', 'POST'])
def projet(idproj):
    form = None
    if 'formavis' in request.values:
        avis = Avis()
        avis.id_projet = idproj
        form = FormAvis(request.form, avis, meta={
            'csrf_context': session,
            'csrf_secret' : current_app.config['CSRF_SECRET'],
            'csrf_time_limit': timedelta(minutes=current_app.config['CSRF_MINUTES'])
        })
        if request.method == 'POST':
            if 'contact' in request.values and contact(projet.titre):
                return redirect(url_for('portfolio.projet', idproj=idproj))
            if 'avis' in request.values and form.validate():
                form.populate_obj(avis)
                db.session.add(avis)
                db.session.commit()
                flash("Merci pour votre retour ! Votre avis apparaîtra dés sa validation.", 'success')
                return redirect(url_for('portfolio.projet', idproj=idproj))
    if 'idavis' in request.args:
        idavis = request.args.get('idavis')
        avis = db.get_or_404(Avis, idavis)
        if 'likes' not in session:
            session['likes'] = []    
        if idavis in session['likes']:
            flash(f"Déjà fait ! Votre like pour l'avis de {avis.auteur} a déjà été pris en compte.", 'warning')
            return redirect(url_for('portfolio.projet', idproj=idproj))
        session['likes'].append(idavis)
        avis.likes += 1
        flash(f"Et de {avis.likes} ! Votre like sur l'avis de {avis.auteur} est comptabilisé.", 'success')
        db.session.commit()
        return redirect(url_for('portfolio.projet', idproj=idproj, _anchor='liste-avis'))
    projet = db.get_or_404(Projet, idproj)
    return render_template('portfolio/projet.html', projet=projet, formavis=form)
