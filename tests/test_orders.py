import datetime
import pytest

from pywhmcs import exceptions


class TestOrderCreate:

    def test_create(self, whmcs_client, client_account, product):
        date = datetime.datetime.today().date()

        order = whmcs_client.orders.create(
            client_id=client_account.id,
            payment_method='mailin',
            product_id=product.id,
            no_email=True,
            price_override=5
        )

        assert order.id
        assert order.client_id == client_account.id
        assert order.amount == 5.0


class TestOrders:

    def test_get(self, whmcs_client, client_account, order):
        order = whmcs_client.orders.get(order.id)

        assert order.id
        assert order.client_id == client_account.id
        assert order.amount == 5.0

    def test_accept(self, whmcs_client, order):
        whmcs_client.orders.accept(order)

        order = whmcs_client.orders.get(order.id)

        assert order.status.lower() == 'active'

    @pytest.mark.skip(reason='Not implemented')
    def test_list(self, whmcs_client, order):
        matches = whmcs_client.orders.list()
        assert order.id in [order.id for order in matches]

    @pytest.mark.skip(reason='Not implemented')
    def test_list_with_filter(self, whmcs_client, client_account, order):
        matches = whmcs_client.orders.list(order_id=order.id)
        assert order.id in [order.id for order in matches]

        matches = whmcs_client.orders.list(client_id=client_account.id)
        assert order.id in [order.id for order in matches]


class TestOrderCancel:

    def test_cancel(self, whmcs_client, order):
        whmcs_client.orders.cancel(order)

        order = whmcs_client.orders.get(order.id)

        assert order.status.lower() == 'cancelled'


class TestOrderDelete:

    def test_delete(self, whmcs_client, order):
        whmcs_client.orders.cancel(order)
        whmcs_client.orders.delete(order)

        with pytest.raises(exceptions.OrderNotFound):
            whmcs_client.orders.get(order.id)
