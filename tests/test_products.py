import pytest


class TestProducts:

    def test_get(self, config, whmcs_client):
        product = whmcs_client.products.get(config.getint('whmcs', 'product_id'))

        assert product.id
        assert product.name
        assert product.type

    def test_list(self, config, whmcs_client, product):
        matches = whmcs_client.products.list()

        assert product.id in [product.id for product in matches]

    def test_list_with_filter(self, config, whmcs_client, product):
        matches = whmcs_client.products.list(product_id=product.id)
        assert product.id in [product.id for product in matches]

        matches = whmcs_client.products.list(group_id=product.group_id)
        assert product.id in [product.id for product in matches]

        matches = whmcs_client.products.list(module=product.module)
        assert product.id in [product.id for product in matches]
