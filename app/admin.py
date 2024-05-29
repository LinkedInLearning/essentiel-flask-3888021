from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from app.modeles import Projet, Avis, Contact, db
from app.forms import FormAvis
from os import path
from datetime import timedelta

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route("/")
def admin():
    return render_template(
        'admin.html', 
        avis = db.session
            .query(Avis)
            .filter_by(ok=False), # .where(Avis.ok == False)
        contacts = db.session
            .query(Contact)
            .order_by(Contact.creation.desc())
            .limit(app.config['PORTFOLIO_ADMIN_MAXCONTACT']),
        utilisateurs = []
    )


@bp.route("/avis/<int:idavis>/ok")
def admin_avis_ok(idavis):
    avis = db.get_or_404(Avis, idavis)
    avis.ok = True
    db.session.commit()
    flash("Approuvé ! L'avis est maintenant en ligne.", 'success')
    return redirect(url_for('admin', _anchor='moderation'))


@bp.route("/avis/<int:idavis>/suppr")
def admin_avis_suppr(idavis):
    avis = db.get_or_404(Avis, idavis)
    db.session.delete(avis)
    db.session.commit()
    flash("Supprimé ! L'avis est bien supprimé.", 'success')
    return redirect(url_for('admin', _anchor='moderation'))


@bp.route("/contact/<int:idcontact>/suppr")
def admin_contact_suppr(idcontact):
    contact = db.get_or_404(Contact, idcontact)
    db.session.delete(contact)
    db.session.commit()
    flash("Supprimé ! La demande de contact est bien supprimée.", 'success')
    return redirect(url_for('admin', _anchor='contacts'))
