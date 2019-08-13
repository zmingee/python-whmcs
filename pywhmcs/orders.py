from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
import dataclasses
import datetime

from pywhmcs import base
from pywhmcs import exceptions


@dataclasses.dataclass
class Order(base.BaseResource):
    id: int
    amount: float
    client_id: int
    contact_id: Optional[int]
    currency_prefix: str
    currency_suffix: str
    date: datetime.datetime
    fraud_data: Optional[str]
    fraud_module: Optional[str]
    fraud_output: Optional[str]
    invoice_id: int
    ip_address: str
    line_items: List[Dict[str, str]]
    name: str
    nameservers: Optional[str]
    notes: Optional[str]
    order_data: str
    order_num: int
    payment_method: str
    payment_method_name: str
    payment_status: str
    promo_code: Optional[str]
    promo_type: Optional[str]
    promo_value: Optional[float]
    renewals: Optional[str]
    status: str
    transfer_secret: Optional[str]

    def accept(self) -> None:
        self.bridge.accept(self)

    def cancel(self,
               resource: Union[int, Order],
               cancel_subscriptions: Optional[bool] = None,
               no_email: Optional[bool] = None) -> None:
        self.bridge.cancel(self)


class OrdersBridge(base.BaseBridge):

    def create(self,
               client_id: int,
               payment_method: str,
               product_id: Optional[int] = None,
               affiliate_id: Optional[int] = None,
               billing_cycle: Optional[str] = None,
               client_ip: Optional[str] = None,
               custom_fields: Optional[Dict[Any, Any]] = None,
               hostname: Optional[str] = None,
               no_email: Optional[bool] = None,
               no_invoice: Optional[bool] = None,
               price_override: Optional[float] = None,
               promo_code: Optional[str] = None,
               promo_override: Optional[bool] = None) -> Dict[str, Any]:
        """
        Create/Add order for client.

        :param int client_id: ID of client for which to create order
        :param str payment_method: Order payment method
        :param int product_id: Product ID to associate with order
        :param int affiliate_id: Affiliate ID to associate with order
        :param str billing_cycle: Billing cycle
        :param str client_ip: IP of the client
        :param dict custom_fields: Custom fields to associate with the order
        :param str hostname: Hostname to associate with order service
        :param bool no_email: Pass ``True`` to suppress email generation
        :param bool no_invoice: Pass ``True`` to suppress invoice generation
        :param float price_override: Override the price of the product being
            ordered.
        :param str promo_code: Promo code to apply to the order
        :param bool promo_override: Pass ``True`` to force promo code accept
        :return: Order
        :rtype: :class:`Order`
        """

        params = {
            key: value for (key, value) in {
                'affid': affiliate_id,
                'billingcycle': billing_cycle,
                'clientid': client_id,
                'clientip': client_ip,
                'hostname': hostname,
                'noemail': no_email,
                'noinvoiceemail': no_invoice,
                'paymentmethod': payment_method,
                'pid': product_id,
                'priceoverride': price_override,
                'promocode': promo_code,
                'promooverride': promo_override,
            }.items() if value is not None
        }

        response = self.client.send_request('addorder', params=params)

        order = self.get(response['orderid'])

        return order

    def get(self, resource: int) -> None:
        """
        Get order via WHMCS API method ``GetOrders``.

        :param str resource: ID of resource to get
        :return: Order
        :rtype: Dict
        """

        response = self.client.send_request(
            'getorders',
            params={'id': resource}
        )

        if not response['numreturned']:
            raise exceptions.OrderNotFound

        whmcs_order = response['orders']['order'][0]

        order = Order(
            self,
            id=int(whmcs_order['id']),
            amount=float(whmcs_order['amount']),
            client_id=int(whmcs_order['userid']),
            contact_id=int(whmcs_order['contactid']) or None,
            currency_prefix=whmcs_order['currencyprefix'],
            currency_suffix=whmcs_order['currencysuffix'],
            date=datetime.datetime.strptime(whmcs_order['date'], '%Y-%m-%d %H:%M:%S'),
            fraud_data=whmcs_order['frauddata'] or None,
            fraud_module=whmcs_order['fraudmodule'] or None,
            fraud_output=whmcs_order['fraudoutput'] or None,
            invoice_id=int(whmcs_order['invoiceid']),
            ip_address=whmcs_order['ipaddress'],
            line_items=whmcs_order['lineitems'],
            name=whmcs_order['name'],
            nameservers=whmcs_order['nameservers'] or None,
            notes=whmcs_order['notes'] or None,
            order_data=whmcs_order['orderdata'],
            order_num=int(whmcs_order['ordernum']),
            payment_method=whmcs_order['paymentmethod'],
            payment_method_name=whmcs_order['paymentmethodname'],
            payment_status=whmcs_order['paymentstatus'],
            promo_code=whmcs_order['promocode'] or None,
            promo_type=whmcs_order['promotype'] or None,
            promo_value=whmcs_order['promovalue'] or None,
            renewals=whmcs_order['renewals'] or None,
            status=whmcs_order['status'],
            transfer_secret=whmcs_order['transfersecret'] or None,
        )

        return order

    def accept(self, resource: Union[int, Order]) -> None:
        """
        Accept an order.

        :pattern str resource: Order (or its ID) to accept
        :return: Does not return
        :rtype: None
        """

        self.client.send_request(
            'acceptorder',
            params={'orderid': base.getid(resource)}
        )

    def delete(self, resource: Union[int, Order]) -> None:
        """
        Delete an order.

        :param str resource: Order (or its ID) to delete
        :return: Does not return
        :rtype: None
        """

        self.client.send_request(
            'deleteorder',
            params={'orderid': base.getid(resource)}
        )

    def cancel(self,
               resource: Union[int, Order],
               cancel_subscriptions: Optional[bool] = None,
               no_email: Optional[bool] = None) -> None:
        """
        Cancel an order.

        :param str order_id: Order (or its ID) to cancel
        :param bool cancel_subscriptions: Pass ``True`` to cancel associated
            product subscriptions
        :param bool no_email: Pass ``True`` to suppress email generation
        :return: Does not return
        :rtype: None
        """

        params = {
            key: value for (key, value) in {
                'cancelsub': cancel_subscriptions,
                'noemail': no_email,
                'orderid': base.getid(resource)
            }.items() if value is not None
        }

        self.client.send_request('cancelorder', params=params)




