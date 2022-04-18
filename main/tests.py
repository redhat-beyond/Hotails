import pytest


@pytest.mark.django_db
class TestViews:
    def test_redirected_to_about_section(self, client):
        response = client.get('/about')
        assert response.status_code == 301
        response = client.get(response.url)
        assert response.status_code == 200

    def test_redirected_to_homepage(self, client):
        response = client.get('')
        assert response.status_code == 200
