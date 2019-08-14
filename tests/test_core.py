import pytest

from pywhmcs import client


class TestClient:

    def test_client_setup(self, config):
        c = client.Client(
            config['whmcs']['api_url'],
            username=config['whmcs']['username'],
            password=config['whmcs']['password']
        )
