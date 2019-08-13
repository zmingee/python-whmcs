import pytest

from pywhmcs import exceptions


class TestTicketCreate:

    def test_create(self, whmcs_client, client_account):
        ticket = whmcs_client.tickets.create(
            'Unit Test Ticket',
            'This is a test ticket',
            dept_id=1,
            client_id=client_account.id,
            admin=True
        )

        assert ticket
        assert ticket.status == 'open'
        assert ticket.client_id == client_account.id


class TestTickets:

    def test_get(self, whmcs_client, client_account, ticket):
        ticket = whmcs_client.tickets.get(ticket.id)

        assert ticket
        assert ticket.status == 'open'
        assert ticket.client_id == client_account.id


class TestTicketDelete:

    def test_delete(self, whmcs_client, client_account):
        ticket = whmcs_client.tickets.create(
            'Unit Test Ticket',
            'This is a test ticket',
            dept_id=1,
            client_id=client_account.id,
            admin=True
        )

        whmcs_client.tickets.delete(ticket)

        with pytest.raises(exceptions.TicketNotFound):
            whmcs_client.tickets.get(ticket.id)
