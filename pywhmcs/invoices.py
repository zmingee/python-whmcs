from typing import Any, List, Optional, Tuple, Union
import dataclasses
import datetime

from pywhmcs import base


@dataclasses.dataclass
class Invoice(base.BaseResource):
    id: int
    balance: float
    cc_gateway: bool
    client_id: int
    credit: float
    date: str
    date_due: str
    date_paid: str
    invoice_num: str
    items: List[Any]
    notes: str
    payment_method: str
    status: str
    subtotal: float
    tax2: float
    tax: float
    taxrate2: float
    taxrate: float
    total: float
    transactions: List[Any]

    def capture_payment(self, cvv: Optional[str] = None) -> None:
        self.bridge.capture_payment(self, cvv)


class InvoiceBridge(base.BaseBridge):

    def update(self, resource: Union[Invoice, int], **kwargs) -> None:
        """
        Update invoice.

        :param resource: Invoice (or its ID) to update
        :param str status: Invoice status
        :param str payment_method: Invoice payment method
        :param float tax_rate: First level invoice tax rate
        :param float tax_rate2: Second level invoice tax rate
        :param float credit: Applied invoice credit
        :param date: Invoice date created
        :param date_due: Invoice date due
        :param date_paid: Invoice date paid
        :param str notes: Invoice notes
        :param items: List of invoice items
        :param new_items: List of new invoice items
        :param bool publish: Publish the invoice
        :param bool publish_and_send: Publish and send the invoice
        """

        params = {
            key: value for (key, value)
            in {
                'invoiceid': base.getid(resource),
                'status': kwargs.get('status'),
                'paymentmethod': kwargs.get('payment_method'),
                'taxrate': kwargs.get('tax_rate'),
                'taxrate2': kwargs.get('tax_rate2'),
                'credit': kwargs.get('credit'),
                'notes': kwargs.get('notes'),
                'publish': kwargs.get('publish'),
                'publishandsendemail': kwargs.get('publish_and_send')
            }.items() if value is not None
        }

        if kwargs.get('date'):
            params['date'] = kwargs['date'].strftime('%Y-%m-%d')

        if kwargs.get('date_due'):
            params['duedate'] = kwargs['date_due'].strftime('%Y-%m-%d')

        if kwargs.get('date_paid'):
            params['datepaid'] = kwargs['date_paid'].strftime('%Y-%m-%d')

        self.client.send_request(action='updateinvoice', params=params)

    def get(self, resource: Union[int, str]) -> Invoice:
        """
        Get an invoice via WHMCS API method ``GetInvoice``.

        :param str resource: ID of invoice to retrieve
        :return: Invoice
        :rtype: :class:`Invoice`
        """

        response = self.client.send_request(
            'getinvoice',
            params={'invoiceid': int(resource)}
        )

        try:
            date_paid = datetime.datetime.strptime(
                response['datepaid'],
                '%Y-%m-%d %H:%M:%S'
            ).date(),
        except ValueError:
            date_paid = None

        invoice = Invoice(
            self,
            balance=float(response.get('balance', 0.0)),
            cc_gateway=response.get('ccgateway'),
            client_id=int(response['userid']),
            credit=float(response['credit']),
            date=datetime.datetime.strptime(response['date'], '%Y-%m-%d').date(),
            date_due=datetime.datetime.strptime(response['duedate'], '%Y-%m-%d').date(),
            date_paid=date_paid,
            id=int(response['invoiceid']),
            invoice_num=response['invoicenum'],
            items=response['items']['item'] if response.get('items') else None,
            notes=response['notes'],
            payment_method=response['paymentmethod'],
            status=response['status'].lower(),
            subtotal=float(response['subtotal']),
            tax2=float(response['tax2']),
            tax=float(response['tax']),
            taxrate2=float(response['taxrate2']),
            taxrate=float(response['taxrate']),
            total=float(response['total']),
            transactions=response.get('transactions', []),
        )

        return invoice

    def list(self, detailed=True, marker=None, limit=None, **filters) -> List[Union[Invoice, str]]:
        """
        List and filter invoices.

        :param int idx: Offset index for index list
        :param int limit: Number of invoices to return in list
        :param int client_id: Client ID to filter by
        :param str status: Status to filter by
        :return: Invoices matching given criteria
        :rtype: List[:class:`Invoice`]
        """

        params = {
            key: value for (key, value)
            in {
                'userid': filters.get('client_id'),
                'status': filters.get('status'),
                'limitstart': marker,
                'limitnum': limit
            }.items() if value is not None
        }

        response = self.client.send_request('getinvoices', params)

        matches = []
        for whmcs_invoice in response['invoices']['invoice']:
            try:
                date_paid = datetime.datetime.strptime(
                    whmcs_invoice['datepaid'],
                    '%Y-%m-%d %H:%M:%S'
                ).date(),
            except ValueError:
                date_paid = None

            invoice = Invoice(
                self,
                balance=float(whmcs_invoice.get('balance', 0.0)),
                cc_gateway=whmcs_invoice.get('ccgateway'),
                client_id=int(whmcs_invoice['userid']),
                credit=float(whmcs_invoice['credit']),
                date=datetime.datetime.strptime(whmcs_invoice['date'], '%Y-%m-%d').date(),
                date_due=datetime.datetime.strptime(whmcs_invoice['duedate'], '%Y-%m-%d').date(),
                date_paid=date_paid,
                id=int(whmcs_invoice['id']),
                invoice_num=whmcs_invoice['invoicenum'],
                items=whmcs_invoice['items']['item'] if whmcs_invoice.get('items') else None,
                notes=whmcs_invoice['notes'],
                payment_method=whmcs_invoice['paymentmethod'],
                status=whmcs_invoice['status'].lower(),
                subtotal=float(whmcs_invoice['subtotal']),
                tax2=float(whmcs_invoice['tax2']),
                tax=float(whmcs_invoice['tax']),
                taxrate2=float(whmcs_invoice['taxrate2']),
                taxrate=float(whmcs_invoice['taxrate']),
                total=float(whmcs_invoice['total']),
                transactions=whmcs_invoice.get('transactions', []),
            )
            matches.append(invoice)

        return matches

    def create(self,
               client_id: Union[int, str],
               status: Optional[str] = None,
               draft: Optional[bool] = None,
               send_invoice: Optional[bool] = None,
               payment_method: Optional[str] = None,
               tax_rate: Optional[float] = None,
               tax_rate2: Optional[float] = None,
               date: Optional[datetime.datetime] = None,
               date_due: Optional[datetime.datetime] = None,
               notes: Optional[str] = None,
               apply_credit: Optional[bool] = None,
               items: Optional[List[Tuple[str]]] = None) -> Invoice:
        params = {
            key: value for (key, value)
            in {
                'userid': int(client_id),
                'status': status,
                'draft': draft,
                'sendinvoice': send_invoice,
                'paymentmethod': payment_method,
                'taxrate': tax_rate,
                'taxrate2': tax_rate2,
                'date': date.strftime('%Y-%m-%d'),
                'duedate': date_due.strftime('%Y-%m-%d'),
                'notes': notes,
                'autoapplycredit': apply_credit
            }.items() if value is not None
        }

        if items is not None:
            for (idx, item) in enumerate(items):
                params[f'itemdescription{idx}'] = item[0]
                params[f'itemamount{idx}'] = item[1]
                params[f'itemtaxed{idx}'] = item[2]

        response = self.client.send_request('createinvoice', params)

        invoice = self.get(response['invoiceid'])

        return invoice

    def capture_payment(self, resource: Union[int, Invoice], cvv: Optional[str] = None) -> None:
        """
        Capture payment on invoice.

        :param str cvv: CVV/CSC for the user's credit card on file if applicable
        :return: None
        :rtype: None
        """

        params = {
            key: value for (key, value) in {
                "invoiceid": base.getid(resource),
                "cvv": cvv
            }.items() if value is not None
        }

        self.client.send_request("capturepayment", params=params)
