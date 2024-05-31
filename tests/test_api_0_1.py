from flask_jwt_extended import create_access_token


def test_projet_avis_get_inexistant(client):
  reponse = client.get('/v0.1/projets/123/avis')
  assert 404 == reponse.status_code


def test_projet_avis_get_existant(client):
  reponse = client.get('/v0.1/projets/1/avis')
  assert 200 == reponse.status_code
  assert 3 == len(reponse.json)


def test_contacts_get_aucun_token(client):
  reponse = client.get('/v0.1/contacts')
  assert 401 == reponse.status_code


def test_contacts_get_mauvais_token(client):
  reponse = client.get('/v0.1/contacts', headers={
    'Authorization': 'Bearer xyz'
  })
  assert 422 == reponse.status_code


def test_contacts_get_token_client(app, client):
  with app.app_context():
    jeton = create_access_token(identity={
        'email': 'xxx',
        'roles': ['client']
    })
  reponse = client.get('/v0.1/contacts', headers={
    'Authorization': f'Bearer {jeton}'
  })
  assert 403 == reponse.status_code


def test_contacts_get_token_admin(app, client):
  with app.app_context():
    jeton = create_access_token(identity={
        'email': 'xxx',
        'roles': ['admin']
    })
  reponse = client.get('/v0.1/contacts', headers={
    'Authorization': f'Bearer {jeton}'
  })
  assert 200 == reponse.status_code
