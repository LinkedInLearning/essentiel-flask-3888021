from flask import Blueprint
from app.modeles import db, Projet

bp = Blueprint('api_0_1', __name__, url_prefix='/v0.1')


@bp.errorhandler(400)
@bp.errorhandler(401)
@bp.errorhandler(403)
@bp.errorhandler(404)
def erreur(e):
    return { 'error': str(e) }, e.code


@bp.get('/projets/<int:idprojet>/avis')
def projets_avis_get(idprojet):
  projet = db.get_or_404(Projet, idprojet)
  return [{ 
    'auteur': a.auteur, 'contenu': a.contenu, 'likes': a.likes 
  } for a in projet.avis if a.ok]