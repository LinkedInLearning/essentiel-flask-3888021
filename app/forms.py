from wtforms import Form, StringField, TextAreaField, validators, ValidationError
from wtforms.csrf.session import SessionCSRF
from flask import current_app


def info_perso(form, field):
    if any(tabou in field.data for tabou in current_app.config['PORTFOLIO_INFO_PERSO']):
        raise ValidationError(f"Pas d'information personnelle dans '{ field.label.text }', s'il vous plait.")


class FormAvis(Form):
    class Meta:
        csrf = True
        csrf_class = SessionCSRF

    auteur = StringField('Nom (entreprise)', [
        validators.InputRequired(),
        validators.Length(min=2, max=50),
        info_perso
    ])
    contenu = TextAreaField('Votre avis', [
        validators.InputRequired(),
        info_perso
    ])

