from flask import Flask, render_template, request, session
from flask_security import Security, SQLAlchemyUserDatastore, hash_password
from flask_babel import Babel
from flask_mailman import Mail
from app.modeles import db, Utilisateur, Role
from os import path
from app import admin, client, portfolio, api_0_1


def create_app():
    app = Flask(__name__, 
                instance_path=path.abspath('instance'), 
                instance_relative_config=True)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    Babel(app)
    # Mail(app)

    app.security = Security(
        app, SQLAlchemyUserDatastore(db, Utilisateur, Role)
    )

    with app.app_context():
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

    app.add_url_rule("/", endpoint="portfolio.index")

    return app
