from __future__ import annotations
from typing import Dict, List, Optional, Union
import dataclasses

from pywhmcs import base
from pywhmcs import exceptions


@dataclasses.dataclass
class ClientResource(base.BaseResource):
    bridge: dataclasses.InitVar[ClientBridge]
    # User information
    id: int
    user_id: int
    uuid: str
    email: str
    first_name: str
    last_name: str
    full_name: str

    # Billing info
    company_name: Optional[str]
    address1: str
    address2: Optional[str]
    city: str
    state: str
    state_code: str
    full_state: str
    post_code: str
    country: str
    country_code: str
    country_name: str
    billing_cid: str
    currency: int
    currency_code: str
    credit: float
    cc_last_four: str
    cc_type: str
    disable_auto_cc: bool
    phone_cc: int
    tax_exempt: bool

    # Contact
    phone_number: str
    phone_number_formatted: str

    # Other
    email_opt_out: bool
    allow_single_sign_on: str
    default_gateway: Optional[str]
    group_id: str
    language: Optional[str]
    last_login: str
    late_fee_overide: bool
    notes: str
    override_due_notices: bool
    override_auto_close: bool
    password: str
    security_q_id: int
    security_q_ans: str
    separate_invoices: bool
    status: str
    twofa_enabled: bool
    custom_fields: List[Dict[str, str]]


class ClientBridge(base.BaseBridge):

    def get(self, resource: Union[str, int]) -> ClientResource:
        """
        Get a :class:`ClientResource` from WHMCS.

        :param resource: ID or email of client to get
        :return: Client
        :rtype: :client:`ClientResource`
        :raises: :class:`pywhmcs.exceptions.ClientNotFound`
        """

        try:
            response = self.client.send_request(
                action='GetClientsDetails',
                params={'clientid': int(resource)}
            )
        except ValueError:
            response = self.client.send_request(
                action='GetClientsDetails',
                params={'email': resource}
            )

        if (response.get('result') == 'error'
                and response['message'].lower() == 'client not found'):
            raise exceptions.ClientNotFound
        elif response.get('result') == 'error':
            raise exceptions.UnknownError(response['message'])

        client = ClientResource(
            self,
            id=int(response['id']),
            user_id=response['userid'],
            uuid=response['uuid'],
            email=response['email'],
            first_name=response['firstname'],
            last_name=response['lastname'],
            full_name=response['fullname'],
            company_name=response['companyname'],
            address1=response['address1'],
            address2=response['address2'],
            city=response['city'],
            state=response['state'],
            state_code=response['statecode'],
            full_state=response['fullstate'],
            post_code=response['postcode'],
            country=response['country'],
            country_code=response['countrycode'],
            country_name=response['countryname'],
            billing_cid=response['billingcid'],
            currency=response['currency'],
            currency_code=response['currency_code'],
            credit=response['credit'],
            cc_last_four=response['cclastfour'],
            cc_type=response['cctype'],
            disable_auto_cc=response['disableautocc'],
            phone_cc=response['phonecc'],
            tax_exempt=response['taxexempt'],
            phone_number=response['phonenumber'],
            phone_number_formatted=response['phonenumberformatted'],
            email_opt_out=response['emailoptout'],
            allow_single_sign_on=response['allowSingleSignOn'],
            default_gateway=response['defaultgateway'],
            group_id=response['groupid'],
            language=response['language'],
            last_login=response['lastlogin'],
            late_fee_overide=response['latefeeoveride'],
            notes=response['notes'],
            override_due_notices=response['overideduenotices'],
            override_auto_close=response['overrideautoclose'],
            password=response['password'],
            security_q_id=response['securityqid'],
            security_q_ans=response['securityqans'],
            separate_invoices=response['separateinvoices'],
            status=response['status'],
            twofa_enabled=response['twofaenabled'],
            custom_fields=response['customfields']
        )

        return client
