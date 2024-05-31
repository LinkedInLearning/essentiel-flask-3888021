from flask import Blueprint, render_template, current_app, request, redirect, url_for, flash
from app.modeles import Avis, Contact, db, Utilisateur
from flask_security import roles_required, hash_password, current_user
from flask_jwt_extended import create_access_token
from re import search

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route("/", methods=['GET', 'POST'])
@roles_required('admin')
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        passe = request.form.get('passe')
        logo = request.form.get('logo')
        if email and passe\
        and logo and search('^img/logos/[a-z]+\.png$', logo):
            current_app.security.datastore.create_user(
                email=email,
                password=hash_password(passe),
                roles=['client'],
                logo=logo)
            db.session.commit()

    return render_template(
        'admin/index.html', 
        avis = db.session
            .query(Avis)
            .filter_by(ok=False), # .where(Avis.ok == False)
        contacts = db.session
            .query(Contact)
            .order_by(Contact.creation.desc())
            .limit(current_app.config['PORTFOLIO_ADMIN_MAXCONTACT']),
        utilisateurs = db.session.query(Utilisateur),
        jwt = create_access_token(identity={
            'email': current_user.email,
            'roles': [ r.name for r in current_user.roles ]
        })
    )


@bp.route("/avis/<int:idavis>/ok")
@roles_required('admin')
def avis_ok(idavis):
    avis = db.get_or_404(Avis, idavis)
    avis.ok = True
    db.session.commit()
    flash("Approuvé ! L'avis est maintenant en ligne.", 'success')
    return redirect(url_for('admin.index', _anchor='moderation'))


@bp.route("/avis/<int:idavis>/suppr")
@roles_required('admin')
def avis_suppr(idavis):
    avis = db.get_or_404(Avis, idavis)
    db.session.delete(avis)
    db.session.commit()
    flash("Supprimé ! L'avis est bien supprimé.", 'success')
    return redirect(url_for('admin.index', _anchor='moderation'))


@bp.route("/contact/<int:idcontact>/suppr")
@roles_required('admin')
def contact_suppr(idcontact):
    contact = db.get_or_404(Contact, idcontact)
    db.session.delete(contact)
    db.session.commit()
    flash("Supprimé ! La demande de contact est bien supprimée.", 'success')
    return redirect(url_for('admin.index', _anchor='contacts'))
