from flask import Flask, render_template, request, session
from flask_security import Security, SQLAlchemyUserDatastore, hash_password
from flask_babel import Babel
from flask_jwt_extended import JWTManager
from app.modeles import db, Utilisateur, Role, Projet, projets, Avis, avis
from app.services import cache
from app import admin, client, portfolio, api_0_1
from flask.cli import with_appcontext
from os import path
import click


def create_app(conf = None):
    app = Flask(__name__, 
                instance_path=path.abspath('instance'), 
                instance_relative_config=True)
    app.config.from_pyfile('config.py')
    if conf:
        app.config.update(conf)
    app.logger.setLevel(app.config['PORTFOLIO_NIVEAU_LOG'])
    
    db.init_app(app)
    cache.init_app(app)

    Babel(app)

    app.security = Security(
        app, SQLAlchemyUserDatastore(db, Utilisateur, Role)
    )
    JWTManager(app)
    app.logger.info('Sécurité ok')

    with app.app_context():
        if app.config['TESTING']:
            db.create_all()
            db.session.add_all([Projet(**p) for p in projets])
            db.session.add_all([Avis(**(a|{'ok':True})) for a in avis])
            db.session.commit()
        app.security.datastore.find_or_create_role(name="admin")
        app.security.datastore.find_or_create_role(name="client")
        db.session.commit()
        admin_mail = app.config['ADMIN_MAIL']
        if not app.security.datastore.find_user(email=admin_mail):
            app.security.datastore.create_user(
                email=admin_mail,
                password=hash_password(app.config['ADMIN_PASSE_INITIAL']),
                roles=['admin'],
                logo=app.config['ADMIN_LOGO'])
            db.session.commit()

    @app.errorhandler(404)
    @app.route("/oups")
    def introuvable(e=None):
      return render_template('introuvable.html')

    @app.before_request
    def cookie_pref():
        if 'cookies' in request.args:
            pref = request.args['cookies']
            session['cookies'] = pref
            session.permanent = pref == 'y'

    app.register_blueprint(admin.bp)
    app.register_blueprint(client.bp)
    app.register_blueprint(portfolio.bp)
    app.register_blueprint(api_0_1.bp)

    app.add_url_rule("/", endpoint="portfolio.index", methods=['GET', 'POST'])

    @app.cli.command(help="Modifie un mot de passe utilisateur.")
    @click.argument('email')
    @click.argument('passe')
    @with_appcontext
    def mdp(email, passe):
        utilisateur = app.security.datastore.find_user(email=email)
        if not utilisateur:
            print("Utilisateur inconnu.")
            return -1
        utilisateur.password = hash_password(passe)
        db.session.commit()
        print("Mot de passe modifié avec succès.")

    return app
