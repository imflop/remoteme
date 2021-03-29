import pytest


class TestAdvertList:
    adverts_list_endpoint = "/api/v1/adverts/list"

    def test_list(self, api_client):
        response = api_client.get(self.adverts_list_endpoint)
        assert response.status_code == 200

    def test_list_unexpected_method(self, api_client):
        response = api_client.post(self.adverts_list_endpoint, data={})
        assert response.status_code == 405
