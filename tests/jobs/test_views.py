import pytest


class TestAdvertList:
    adverts_list_endpoint = "/api/v1/adverts/list"

    def test_list(self, api_client):
        response = api_client.get(self.adverts_list_endpoint)
        assert response.status_code == 200
