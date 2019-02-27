from typing import Any, Dict
import hashlib

import requests

from pywhmcs import clients
from pywhmcs import tickets


class Client:

    def __init__(self, api_url: str, username: str, password: str):
        self.api_url = api_url
        self.username = username
        self.password = password

        # Setup bridges
        self.clients = clients.ClientBridge(self)
        self.tickets = tickets.TicketBridge(self)

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

        return content
