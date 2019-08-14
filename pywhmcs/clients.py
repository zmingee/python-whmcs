from __future__ import annotations
from typing import Dict, List, Optional, Union
import dataclasses

from pywhmcs import base


@dataclasses.dataclass
class ClientResource(base.BaseResource):
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

    def create(self,
               email: str,
               password: str,
               first_name: str,
               last_name: str,
               address1: str,
               city: str,
               state: str,
               postcode: str,
               country: str,
               phone_number: str,
               company_name: Optional[str] = None,
               address2: Optional[str] = None,
               currency: Optional[int] = None,
               client_ip: Optional[str] = None,
               language: Optional[str] = None,
               group_id: Optional[str] = None,
               security_q_id: Optional[str] = None,
               security_q_ans: Optional[str] = None,
               notes: Optional[str] = None,
               card_type: Optional[str] = None,
               card_num: Optional[str] = None,
               card_exp_date: Optional[str] = None,
               start_date: Optional[str] = None,
               issue_number: Optional[str] = None,
               custom_fields: Optional[str] = None,
               no_email: Optional[str] = 'true',
               skip_validation: Optional[str] = 'false') -> ClientResource:
        """
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
            'cardtype': card_type,
            'cardnum': card_num,
            'expdate': card_exp_date,
            'startdate': start_date,
            'issuenumber': issue_number,
            'customfields': custom_fields,
            'noemail': no_email,
            'skipvalidation': skip_validation
        }
        params = {k: v for k, v in params.items() if v is not None}

        self.client.send_request(
            action='addclient',
            params=params
        )

        return self.get(email)

    def get(self, resource: Union[str, int]) -> ClientResource:
        """
        Get a :class:`ClientResource` from WHMCS.

        :param resource: ID or email of client to get
        :param: str or int
        :return: Client
        :rtype: :class:`ClientResource`
        :raises: :class:`pywhmcs.exceptions.ClientNotFound`
        :raises: :class:`pywhmcs.exceptions.UnknownError
        """

        try:
            response = self.client.send_request(
                action='getclientsdetails',
                params={'clientid': int(resource)}
            )
        except ValueError:
            response = self.client.send_request(
                action='getclientsdetails',
                params={'email': resource}
            )

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
            status=response['status'].lower(),
            twofa_enabled=response['twofaenabled'],
            custom_fields=response['customfields']
        )

        return client

    def get_products(self,
                     resource: Union[ClientResource, int],
                     service_id: int = None,
                     product_id: int = None) -> dict:
        client_id = base.getid(resource)

        params = {
            k: v for k, v
            in {
                "clientid": client_id,
                "pid": product_id,
                "serviceid": service_id
            }.items() if v is not None
        }

        response = self.client.send_request("getclientsproducts", params)

        if not response["numreturned"]:
            matches = []
        else:
            matches = response["products"]["product"]

        return matches

    def update(self, resource: Union[ClientResource, int], **kwargs) -> None:
        """
        Update WHMCS client account.

        :param resource: Instance or ID of client to update
        """

        params = {
            k: v for (k, v)
            in {
                'clientid': str(base.getid(resource)),
                'address1': kwargs.get('address1'),
                'address2': kwargs.get('address2'),
                'cardnum': kwargs.get('card_num'),
                'cardtype': kwargs.get('card_type'),
                'city': kwargs.get('city'),
                'companyname': kwargs.get('company_name'),
                'country': kwargs.get('country'),
                'credit': kwargs.get('credit'),
                'customfields': kwargs.get('custom_fields'),
                'email': kwargs.get('email'),
                'expdate': kwargs.get('card_exp_date'),
                'firstname': kwargs.get('first_name'),
                'lastname': kwargs.get('last_name'),
                'notes': kwargs.get('notes'),
                'password2': kwargs.get('password'),
                'phonenumber': kwargs.get('phone_number'),
                'postcode': kwargs.get('post_code'),
                'state': kwargs.get('state'),
                'status': kwargs.get('status')
            }.items() if v is not None
        }

        self.client.send_request(
            action='updateclient',
            params=params
        )

    def delete(self, resource: Union[ClientResource, int]) -> None:
        """
        Delete WHMCS client account.

        :param resource: ID  or Instanceof client to delete
        """
        client_id = base.getid(resource)

        self.client.send_request(
            action='deleteclient',
            params={'clientid': client_id}
        )

    def close_client(self, resource: Union[ClientResource, int]) -> None:
        """
        Close WHMCS client account.

        :param resource: :class:`ClientResource` (or its ID) to close
        :rtype: None
        """

        client_id = base.getid(resource)

        self.client.send_request(
            action='closeclient',
            params={'clientid': client_id}
        )

    def add_pay_method(self,
                       resource: Union[ClientResource, int],
                       bank_account: Optional[str] = None,
                       bank_account_type: Optional[str] = None,
                       bank_code: Optional[str] = None,
                       bank_name: Optional[str] = None,
                       card_expiry: Optional[str] = None,
                       card_issue_number: Optional[str] = None,
                       card_number: Optional[str] = None,
                       description: Optional[str] = None,
                       gateway_module_name: Optional[str] = None,
                       method_type: Optional[str] = None,
                       set_as_default: Optional[bool] = None) -> None:
        """
        Add a pay method. Supports bank account and credit card methods.

        :param str method_type: Type of pay method to add
        :param str description: Description of pay method
        :param str gateway_module_name: Name of gateway module for pay method
        :param str card_number: Credit card number. Required for ``CreditCard``
            pay method type
        :param str card_expiry: Credit card expiration date. Required for
            ``CreditCard`` pay method type. Must be in ``MMYY`` format.
        :param str card_issue_number: Credit card issue number
        :param str bank_name: Name of bank for ``BankAccount`` pay method type.
        :param str bank_account_type: Type of bank for ``BankAccount`` pay
            method type, such as checking or credit
        :param str bank_code: Bank code or routing number. Required for
            ``BankAccount`` pay method type.
        :param str bank_account: Bank account number. Required for
            ``BankAccount`` pay method type.
        param bool set_as_default: Set pay method as default.
        """

        raise NotImplementedError('Pending WHMCS v7.8 release - https://docs.whmcs.com/Version_7.8_Release_Notes#Time-Based_Tokens_now_Freely_Available')

        self.client.send_request(
            action='addpaymethod',
            params={
                'clientid': base.getid(resource),
                'bank_account': bank_account,
                'bank_account_type': bank_account_type,
                'bank_code': bank_code,
                'bank_name': bank_name,
                'card_expiry': card_expiry,
                'card_issue_number': card_issue_number,
                'card_number': card_number,
                'description': description,
                'gateway_module_name': gateway_module_name,
                'set_as_default': set_as_default,
                'type': method_type,
            }
        )
