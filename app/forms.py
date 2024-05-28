from wtforms import Form, StringField, TextAreaField

class FormAvis(Form):
    auteur = StringField('Nom (entreprise)')
    contenu = TextAreaField('Votre avis')

