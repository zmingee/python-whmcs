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

    def update(self, **kwargs):
        self.bridge.update_client(self, kwargs)

    def delete(self):
        self.bridge.delete_client(self)

    def save(self):
        raise NotImplementedError

    def enable(self):
        self.bridge.enable(self)

    def disable(self):
        self.bridge.disable(self)


class ClientBridge(base.BaseBridge):

    def create(self, email: str, password: str, first_name: str, last_name: str, address1: str, city: str,
               state: str, postcode: str, country: str, phone_number: str, company_name: str = None,
               address2: str = None, currency: int = None, client_ip: str=None, language: str=None,
               group_id: str = None, security_q_id: str = None, security_q_ans: str = None,
               notes: str=None, cardtype: str = None, cardnum: str = None, expdate: str = None,
               start_date: str = None, issue_number: str = None, custom_fields: str = None,
               no_email: str = 'true', skip_validation: str = 'false') -> ClientResource:
        """
        Create a WHMCS client account

        :param str email: User's email
        :param str password: User's password
        :param str first_name: User's first_name
        :param str last_name: User's last_name
        :param str address1: First line of user's billing address
        :param str city: Billing address city
        :param str state: Billing address state
        :param str postcode: Billing address postal/zip code
        :param str country: Billing address ISO country code
        :param str phone_number: User's contact phone number
        :param str company_name: OPTIONAL - Name of user's company
        :param str address2: OPTIONAL - Second line of user's billing address
        :param int currency: OPTIONAL - Currency ID to assign to client account
        :param str client_ip:
            OPTIONAL - IP address of originating request; used for various
            functionalities such as fraud checking
        :param str language: OPTIONAL - User's defaut language
        :param str group_id: OPTIONAL - Group to assign client account to
        :param str security_q_id:
            OPTIONAL - Security/Verification question ID
        :param str security_q_ans:
            OPTIONAL - Security/Verification question answer
        :param str notes:
            OPTIONAL - Notes to assign to the user's client account
        :param str cardtype: OPTIONAL - Credit card type/provider
        :param str cardnum: OPTIONAL - Credit card number
        :param str expdate: OPTIONAL - Credit card expiration date
        :param str start_date:
            OPTIONAL - Credit card start date (if applicable)
        :param str issuenumber:
            OPTIONAL - Credit card issue number (if applicable)
        :param str cvv:
            OPTIONAL - Credit card CVV/CSC number (will not be stored)
        :param str custom_fields:
            OPTIONAL - Custom fields to set on client account
        :param bool no_email:
            OPTIONAL - Pass as ``True`` to skip sending welcome email
        :param bool skip_validation:
            OPTIONAL - Pass as ``True`` to ignore required fields validation
        :return: New client account
        :rtype: :py:class:`auth.whmcs.Client`

        .. note::
            ``country`` param must be an ISO country code. Please see
            ISO 3166-1 alpha-2 -
            https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
        .. note::
            ``state`` param must be full state name, no abbreviations
        .. note::
            ``language`` param must be full language name: "english", "french",
            etc.
        .. note::
            ``custom_fields`` param must be a Base64 encoded, serialized
            PHP-type array string format (save yourself a headache and just use
            the ``phpserialize`` Python library
        """

        params = {
            'firstname': first_name,
            'lastname': last_name,
            'email': email,
            'address1': address1,
            'city': city,
            'state': state,
            'postcode': postcode,
            'country': country,
            'phonenumber': phone_number,
            'password2': password,
            'companyname': company_name,
            'address2': address2,
            'currency': currency,
            'clientip': client_ip,
            'language': language,
            'groupid': group_id,
            'securityqid': security_q_id,
            'securityqans': security_q_ans,
            'notes': notes,
            'cardtype': cardtype,
            'cardnum': cardnum,
            'expdate': expdate,
            'startdate': start_date,
            'issuenumber': issue_number,
            'customfields': custom_fields,
            'noemail': no_email,
            'skipvalidation': skip_validation
        }
        params = {k: v for k, v in params.items() if v is not None}

        response = self.client.send_request(
            action='addclient',
            params=params
        )

        return self.get(response['clientid'])

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

    def list_clients(self) -> list:
        """
        List WHMCS clients.
        """
        clients = []

        response = self.client.send_request(action='getclients')

        for client in response['clients']['client']:
            clients.append(client)

        return clients

    def get_clients_products(self, resource: Union[ClientResource, int], service_id: int = None, product_id: int = None,
                             start_number: int = 0) -> dict:
        """
        Get products for given client

        :param resource: Client to lookup products for
        :param int service_id: Get product matching given client product ID
        :param int product_id: Limit search to a specific product ID
        :param int start_number: Products index to start lookup on
        :param int limit: Total number of products to return
        :return: Products matching given criteria for the specified client ID
        :rtype: dict
        """
        client_id = base.getid(resource)

        params = {
            k: v for k, v
            in {
            "clientid": client_id,
            "serviceid": service_id,
            "pid": product_id,
            "limitstart": start_number
        }.items()
            if v is not None
        }

        response = self.client.send_request("GetClientsProducts", params)

        if not response["numreturned"]:
            products = []
        else:
            products = response["products"]["product"]

        return {
            "total": int(response["totalresults"]),
            "products": products,
            "start_number": int(response["startnumber"])
        }

    def update_client(self, resource: Union[ClientResource, int], **kwargs) -> None:
        """
            Update WHMCS client account.

            :param resource: Instance or ID of client to update
            """

        accepted_params = [
            "email",
            "password2",
            "firstname",
            "lastname",
            "companyname",
            "address1",
            "address2",
            "city",
            "state",
            "postcode",
            "country",
            "phonenumber",
            "credit",
            "notes",
            "cardtype",
            "cardnum",
            "expdate",
            "status",
            "customfields"
        ]
        params = {k: v for k, v in kwargs.items() if k in accepted_params and v is not None}
        params['clientid'] = str(base.getid(resource))

        response = self.client.send_request(
            action='updateclient',
            params=params
        )
        return response

    def delete_client(self, resource: Union[ClientResource, int]) -> None:
        """
        Delete WHMCS client account.

        :param resource: ID  or Instanceof client to delete
        """
        client_id = base.getid(resource)

        response = self.client.send_request(
            action='DeleteClient',
            params={'clientid': client_id}
        )

        return response

    def close_client(self, resource: Union[ClientResource, int]) -> None:
        """
        Close WHMCS client account.

        :param resource: ID or Instance of client to close
        """
        client_id = base.getid(resource)

        response = self.client.send_request(
            action='CloseClient',
            params={'clientid': client_id,
                    }
        )

        return response

    def enable_client(self, resource: Union[ClientResource, int]) -> None:
        """
        Enable WHMCS client account.

        :param resource: ID or Instance of client to enable
        """

        client_id = base.getid(resource)

        response = self.client.send_request(
            action='updateclient',
            params={
                'clientid': client_id,
                'status': 'Active'
            }
        )
        return response

    def disable_client(self, resource: Union[ClientResource, int]) -> None:
        """
        Disable WHMCS client account.

        :param resource: ID or Instance of client to disable
        """

        client_id = base.getid(resource)

        response = self.client.send_request(
            action='updateclient',
            params={
                'clientid': client_id,
                'status': 'Inactive'
            }
        )
        return response







