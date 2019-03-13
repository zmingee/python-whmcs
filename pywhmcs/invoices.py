
from pywhmcs import base


class InvoiceBridge(base.BaseBridge):

    def get_invoices(self, start_number: int = 0, limit: int = 25, client_id: int = None, status: str = None) -> dict:
        """
        Get invoices matching criteria.

        :param int start_number: Offset for the returned resources
        :param int limit: Number of resources to return
        :param int client_id: Limit query to specific client ID
        :param str status: Limit query to those matching status
        :return: Invoices matching the defined parameters.
        :rtype: dict
        """

        params = {
            "limitstart": start_number,
            "limitnum": limit,
            "userid": client_id,
            "status": status
        }
        params = {k: v for k, v in params.items() if v is not None}

        response = self.client.send_request("GetInvoices", params)

        if not response["numreturned"]:
            invoices = []
        else:
            invoices = response["invoices"]["invoice"]

        return {
            "total": int(response["totalresults"]),
            "invoices": invoices,
            "start_number": int(response["startnumber"])
        }

    def get_invoice(self, invoice_id: int) -> dict:
        """
        Get invoice.

        :param int invoice_id: Invoice to retrieve
        :return: Invoice data
        :rtype: dict
        """

        params = {
            "invoiceid": int(invoice_id)
        }

        response = self.client.send_request("GetInvoice", params)

        return response



