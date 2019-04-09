from __future__ import annotations
from typing import Dict, List, Optional, Union
import dataclasses

from pywhmcs import base
from pywhmcs import exceptions


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
               client_ip: Optional[str]=None,
               language: Optional[str] =None,
               group_id: Optional[str] = None,
               security_q_id: Optional[str] = None,
               security_q_ans: Optional[str] = None,
               notes: Optional[str] =None,
               cc_type: Optional[str] = None,
               cc_pan: Optional[str] = None,
               cc_exp_date: Optional[str] = None,
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
            'cardtype': cc_type,
            'cardnum': cc_pan,
            'expdate': cc_exp_date,
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
            status=response['status'],
            twofa_enabled=response['twofaenabled'],
            custom_fields=response['customfields']
        )

        return client

    # def get_clients_products(self,
    #                          resource: Union[ClientResource, int],
    #                          service_id: int = None,
    #                          product_id: int = None,
    #                          start_number: int = 0) -> dict:
    #     client_id = base.getid(resource)

    #     params = {
    #         k: v for k, v
    #         in {
    #             "clientid": client_id,
    #             "serviceid": service_id,
    #             "pid": product_id,
    #             "limitstart": start_number
    #         }.items() if v is not None
    #     }

    #     response = self.client.send_request("GetClientsProducts", params)

    #     if not response["numreturned"]:
    #         products = []
    #     else:
    #         products = response["products"]["product"]

    #     return {
    #         "total": int(response["totalresults"]),
    #         "products": products,
    #         "start_number": int(response["startnumber"])
    #     }

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
                'cardnum': kwargs.get('cc_pan'),
                'cardtype': kwargs.get('cc_type'),
                'city': kwargs.get('city'),
                'companyname': kwargs.get('company_name'),
                'country': kwargs.get('country'),
                'credit': kwargs.get('credit'),
                'customfields': kwargs.get('custom fields'),
                'email': kwargs.get('email'),
                'expdate': kwargs.get('cc_exp_date'),
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

        response = self.client.send_request(
            action='updateclient',
            params=params
        )

        return self.get(base.getid(resource))

    def delete(self, resource: Union[ClientResource, int]) -> None:
        """
        Delete WHMCS client account.

        :param resource: ID  or Instanceof client to delete
        """
        client_id = base.getid(resource)

        response = self.client.send_request(
            action='deleteclient',
            params={'clientid': client_id}
        )

    def close_client(self, resource: Union[ClientResource, int]) -> None:
        """
        Close WHMCS client account.

        :param resource: ID or Instance of client to close
        """
        client_id = base.getid(resource)

        response = self.client.send_request(
            action='closeclient',
            params={'clientid': client_id}
        )
