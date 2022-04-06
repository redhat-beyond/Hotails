def test_root_entrypoint(client):
    response = client.get("/")
    assert response.status_code == 200
