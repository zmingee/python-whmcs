# pylint: disable=missing-docstring,redefined-outer-name

import configparser
import datetime
import os

import pytest

from pywhmcs import client
from pywhmcs import clients


@pytest.fixture(scope='session')
def config():
    settings_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.cfg')

    cp = configparser.ConfigParser()
    paths = cp.read(settings_path)

    if not paths or not cp.sections():
        raise Exception(f'Unit test config file not found: {settings_path}')

    return cp


@pytest.fixture(scope='session')
def whmcs_client(config):
    return client.Client(
        config['whmcs']['api_url'],
        username=config['whmcs']['username'],
        password=config['whmcs']['password']
    )


@pytest.fixture(scope='class')
def client_stub(whmcs_client):
    stub = {
        'email': 'john.dough@example.com',
        'password': 'Password123',
        'first_name': 'John',
        'last_name': 'Dough',
        'address1': '123 Easy St',
        'city': 'Cincinnati',
        'state': 'Ohio',
        'postcode': '45227',
        'country': 'US',
        'phone_number': '+15131231234'
    }

    yield stub

@pytest.fixture(scope='class')
def client_cleanup(whmcs_client, client_stub):
    yield

    client = whmcs_client.clients.get(client_stub['email'])
    client.delete()


@pytest.fixture(scope='class')
def client_account(whmcs_client, client_stub):
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
        phone_number=client_stub['phone_number'],
        cc_type='Visa',
        cc_pan='4111111111111111',
        cc_exp_date='1222'
    )

    yield client

    client.delete()


@pytest.fixture(scope='class')
def product(config, whmcs_client):
    product = whmcs_client.products.get(config.getint('whmcs', 'product_id'))

    return product


@pytest.fixture(scope='class')
def invoice(whmcs_client, client_account):
    date = datetime.datetime.today().date()
    date_due = date + datetime.timedelta(days=30)

    invoice = whmcs_client.invoices.create(
        client_id=client_account.id,
        send_invoice=False,
        date=date,
        date_due=date_due,
        items=[('Test item', 5.0, False)],
        payment_method='bluepay'
    )

    return invoice


@pytest.fixture(scope='class')
def order(whmcs_client, client_account, product):
    date = datetime.datetime.today().date()

    order = whmcs_client.orders.create(
        client_id=client_account.id,
        payment_method='mailin',
        product_id=product.id,
        no_email=True,
        price_override=5
    )

    return order


@pytest.fixture(scope='class')
def ticket(whmcs_client, client_account):
    ticket = whmcs_client.tickets.create(
        'Unit Test Ticket',
        'This is a test ticket',
        dept_id=1,
        client_id=client_account.id,
        admin=True
    )

    yield ticket

    ticket.delete()
