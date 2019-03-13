
from pywhmcs import base


class BillingBridge(base.BaseBridge):

    def capture_payment(self, invoice_id: int, cvv: str = None) -> None:
        """
        Call WHMCS API method ``CapturePayment``.

        Captures payment for a given invoice using the invoicee's default payment
        method.

        :param int invoice_id: Invoice to capture payment for
        :param str cvv: CVV/CSC for the user's credit card on file if applicable
        :return: None
        :rtype: None
        """

        params = {
            "invoiceid": int(invoice_id),
            "cvv": cvv
        }

        response = self.client.send_request("CapturePayment", params)


