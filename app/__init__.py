from flask import Flask, render_template, request, session
from app.modeles import db
from os import path
from app import admin, portfolio


def create_app():
  app = Flask(__name__, 
              instance_path=path.abspath('instance'), 
              instance_relative_config=True)
  app.config.from_pyfile('config.py')
  db.init_app(app)

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
  app.register_blueprint(portfolio.bp)

  app.add_url_rule("/", endpoint="portfolio.index")
  
  return app
