def test_fumee(client):
  reponse = client.get('/')
  assert 200 == reponse.status_code
