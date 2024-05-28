from wtforms import Form, StringField, TextAreaField
from wtforms.csrf.session import SessionCSRF
from datetime import timedelta


class FormAvis(Form):
    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = b'zYxKxs39RsZ2Xs7EvPXuU6AfON4'
        csrf_time_limit = timedelta(minutes=10)

    auteur = StringField('Nom (entreprise)')
    contenu = TextAreaField('Votre avis')

