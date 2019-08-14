import pytest


class TestPromotions:

    def test_get(self, config, whmcs_client):
        assert whmcs_client.promotions.get(config['whmcs']['promotion_code'])

    def test_list(self, config, whmcs_client):
        matches = whmcs_client.promotions.list()
        assert config['whmcs']['promotion_code'] in [promotion.code for promotion in matches]
