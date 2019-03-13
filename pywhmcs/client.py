from typing import Any, Dict, Optional, Union, List
import hashlib

import requests

from pywhmcs import clients
from pywhmcs import tickets
from pywhmcs import orders
from pywhmcs import billing
from pywhmcs import invoices
from pywhmcs import products
from pywhmcs import promotions
from pywhmcs import exceptions


class Client:

    def __init__(self, api_url: str, username: str, password: str):
        self.api_url = api_url
        self.username = username
        self.password = password

        # Setup bridges
        self.clients = clients.ClientBridge(self)
        self.tickets = tickets.TicketBridge(self)
        self.orders = orders.OrdersBridge(self)
        self.billing = billing.BillingBridge(self)
        self.invoices = invoices.InvoiceBridge(self)
        self.products = products.ProductsBridge(self)
        self.promotions = promotions.PromotionsBridge(self)

    def send_request(self, action: str, params=None) -> Dict[Any, Any]:
        """
        Send request to WHMCS API.

        :param str action: Action to perform
        :param params: API parameters
        :return: Response JSON body
        :rtype: dict
        """

        payload = {
            'username': self.username,
            'password': hashlib.md5(self.password.encode()).hexdigest(),
            'responsetype': 'json',
            'action': action,
        }
        payload.update(params)

        response = requests.post(self.api_url, data=payload)
        content = response.json()

        if content.get('result') == 'error':
            raise exceptions.from_response(content, action)

        return content




