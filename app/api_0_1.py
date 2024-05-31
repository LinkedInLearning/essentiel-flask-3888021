from flask import Blueprint, jsonify, abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.modeles import db, Projet, Contact

bp = Blueprint('api_0_1', __name__, url_prefix='/v0.1')


@bp.errorhandler(400)
@bp.errorhandler(401)
@bp.errorhandler(403)
@bp.errorhandler(404)
def erreur(e):
    return jsonify(error=str(e)), e.code


@bp.get('/projets/<int:idprojet>/avis')
def projets_avis_get(idprojet):
  projet = db.get_or_404(Projet, idprojet)
  return [a.dto() for a in projet.avis if a.ok]


@bp.get('/contacts')
@jwt_required()
def contacts_get():
  identite = get_jwt_identity()
  if 'admin' not in identite['roles']:
     abort(403)
  contacts = db.session.query(Contact)
  return [c.dto() for c in contacts]
