import datetime

import pytest


class TestInvoiceCreate:

    def test_create(self, whmcs_client, client_account):
        date = datetime.datetime.today().date()
        date_due = date + datetime.timedelta(days=30)

        invoice = whmcs_client.invoices.create(
            client_id=client_account.id,
            send_invoice=False,
            date=date,
            date_due=date_due,
        )

        assert invoice.client_id == client_account.id
        assert invoice.date == date
        assert invoice.date_due == date_due


class TestInvoices:

    def test_get(self, whmcs_client, invoice):
        invoice = whmcs_client.invoices.get(invoice.id)

        assert invoice.id
        assert invoice.date == datetime.datetime.today().date()
        assert invoice.date_due == datetime.datetime.today().date() + datetime.timedelta(days=30)

    def test_list(self, config, whmcs_client, client_account, invoice):
        matches = whmcs_client.invoices.list(client_id=client_account.id)
        assert invoice.id in [invoice.id for invoice in matches]

    def test_update(self, config, whmcs_client, invoice):
        whmcs_client.invoices.update(invoice.id, status='Paid')
        invoice = whmcs_client.invoices.get(invoice.id)
        assert invoice.status == 'Paid'

        date = (datetime.datetime.today() + datetime.timedelta(days=1)).date()
        whmcs_client.invoices.update(invoice.id, date=date)
        invoice = whmcs_client.invoices.get(invoice.id)
        assert invoice.date == date

    def test_capture_payment(self, config, whmcs_client, invoice):
        whmcs_client.invoices.capture_payment(invoice)
        invoice = whmcs_client.invoices.get(invoice.id)
        assert invoice.status == 'Paid'
