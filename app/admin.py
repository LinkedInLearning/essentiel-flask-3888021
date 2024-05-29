from flask import Blueprint, render_template, current_app, redirect, url_for, flash
from app.modeles import Avis, Contact, db
from flask_security import auth_required

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route("/")
@auth_required()
def index():
    return render_template(
        'admin/index.html', 
        avis = db.session
            .query(Avis)
            .filter_by(ok=False), # .where(Avis.ok == False)
        contacts = db.session
            .query(Contact)
            .order_by(Contact.creation.desc())
            .limit(current_app.config['PORTFOLIO_ADMIN_MAXCONTACT']),
        utilisateurs = []
    )


@bp.route("/avis/<int:idavis>/ok")
@auth_required()
def avis_ok(idavis):
    avis = db.get_or_404(Avis, idavis)
    avis.ok = True
    db.session.commit()
    flash("Approuvé ! L'avis est maintenant en ligne.", 'success')
    return redirect(url_for('admin.index', _anchor='moderation'))


@bp.route("/avis/<int:idavis>/suppr")
@auth_required()
def avis_suppr(idavis):
    avis = db.get_or_404(Avis, idavis)
    db.session.delete(avis)
    db.session.commit()
    flash("Supprimé ! L'avis est bien supprimé.", 'success')
    return redirect(url_for('admin.index', _anchor='moderation'))


@bp.route("/contact/<int:idcontact>/suppr")
@auth_required()
def contact_suppr(idcontact):
    contact = db.get_or_404(Contact, idcontact)
    db.session.delete(contact)
    db.session.commit()
    flash("Supprimé ! La demande de contact est bien supprimée.", 'success')
    return redirect(url_for('admin.index', _anchor='contacts'))
