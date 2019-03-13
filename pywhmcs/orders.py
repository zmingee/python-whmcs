
from pywhmcs import base


class OrdersBridge(base.BaseBridge):

    def get_orders(self, client_id: int = None, order_id: int = None, status: str = None, start_number: int = 0) -> dict:
        """
        Get orders matching defined criteria

        :param int client_id: Client to lookup orders for
        :param int order_id: Specific order ID to lookup
        :param str status: Find orders matching a specific status
        :param int start_number: Orders index to start lookup on
        :return: Orders in the form of a WHMCS response
        :rtype: dict
        """

        params = {
            r: v for r, v
            in {
                "userid": client_id,
                "id": order_id,
                "status": status,
                "limitstart": start_number
            }.items()
            if v is not None
        }

        response = self.client.send_request("GetOrders", params)

        if not response["numreturned"]:
            orders = []
        else:
            orders = response["orders"]["order"]

        return {
            "total": int(response["totalresults"]),
            "orders": orders,
            "start_number": int(response["startnumber"])
        }

    def add_order(self, client_id: int, product_id: int, payment_method: str, billing_cycle: str = None,
                  affiliate_id: int = None, promo_code: str = None, client_ip: str= None,
                  price_override: float = None, custom_fields: dict = None) -> dict:
        """
        Call WHMCS API method ``AddOrder``.

        Add an order for the specified client.

        :param int client_id: Client to generate an order for
        :param int product_id: Product ID to add the order for
        :param str billing_cycle: Billing cycle
        :param str payment_method: Payment method
        :param int affiliate_id: Affiliate ID to associate with order
        :param str promo_code: Promo code to apply to the order
        :param str client_ip: IP of the client
        :param float price_override:
            Override the price of the product being ordered.
        :param dict custom_fields: Custom fields to associate with the order
        :return: Product
        :rtype: dict
        """

        params = {
            'clientid': client_id,
            'pid': product_id,
            'billingcycle': billing_cycle,
            'paymentmethod': payment_method,
            'noemail': 'true',
            'promocode': promo_code,
            'clientip': client_ip,
            'priceoverride': price_override,
            'affid': affiliate_id,
            'customfields': custom_fields
        }

        response = self.client.send_request("AddOrder", params)

        rv = {
            "order_id": response["orderid"],
            "product_id": response["productids"],
            "invoice_id": response["invoiceid"],
            "domain_id": response["domainids"]
        }

        return rv




