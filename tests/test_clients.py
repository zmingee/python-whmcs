import phonenumbers
import pytest

from pywhmcs import exceptions


class TestClientCreate:

    def test_client_create(self, whmcs_client, client_stub, client_cleanup):
        client = whmcs_client.clients.create(
            email=client_stub['email'],
            password=client_stub['password'],
            first_name=client_stub['first_name'],
            last_name=client_stub['last_name'],
            address1=client_stub['address1'],
            city=client_stub['city'],
            state=client_stub['state'],
            postcode=client_stub['postcode'],
            country=client_stub['country'],
            phone_number=client_stub['phone_number']
        )

        assert client.email == 'john.dough@example.com'


class TestClientDelete:

    def test_client_delete(self, whmcs_client, client_stub):
        client = whmcs_client.clients.create(
            email=client_stub['email'],
            password=client_stub['password'],
            first_name=client_stub['first_name'],
            last_name=client_stub['last_name'],
            address1=client_stub['address1'],
            city=client_stub['city'],
            state=client_stub['state'],
            postcode=client_stub['postcode'],
            country=client_stub['country'],
            phone_number=client_stub['phone_number']
        )

        whmcs_client.clients.delete(client)

        with pytest.raises(exceptions.ResourceNotFound):
            whmcs_client.clients.get(client.id)

class TestClients:

    def test_get(self, whmcs_client, client_account):
        client = whmcs_client.clients.get(client_account.id)

        assert client.id == client_account.id
        assert client.email == client_account.email

    def test_update_phone_number(self, whmcs_client, client_account, faker):
        phone_number = phonenumbers.parse('+15135491234', 'US')

        phone_number_fmt = phonenumbers.format_number(
            phone_number,
            phonenumbers.PhoneNumberFormat.E164
        )

        client_account.update(phone_number=phone_number_fmt)

        client_account = whmcs_client.clients.get(client_account.id)

        assert phonenumbers.parse(client_account.phone_number, 'US') == phone_number

    def test_close_client(self, whmcs_client, client_account):
        whmcs_client.clients.close_client(client_account)

        client_account = whmcs_client.clients.get(client_account.id)

        assert client_account.status.lower() == 'closed'

    @pytest.mark.skip(reason='Pending WHMCS v7.8 release')
    def test_add_pay_method(self, whmcs_client, client_account):
        whmcs_client.clients.add_pay_method(
            client_account,
            method_type='CreditCard',
            card_number='42424242424242424242',
            card_expiry='1222',
            set_as_default=True
        )

        client_account = whmcs_client.clients.get(client_account.id)

        assert client_account.cc_last_four == '4242'
        assert client_account.cc_type.lower() == 'visa'

    def test_get_products(self, whmcs_client, client_account, product, order):
        matches = whmcs_client.clients.get_products(
            client_account,
            product_id=product.id
        )

        assert order.id in [int(product['orderid']) for product in matches]
