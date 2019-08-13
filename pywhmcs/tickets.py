from typing import Any, Dict, List, Optional, Union

import dataclasses
import datetime
import string

from pywhmcs import base


@dataclasses.dataclass
class Ticket(base.BaseResource):
    id: int
    admin: Optional[str]
    cc_email: Optional[str]
    client_id: int
    contact_id: Optional[int]
    date: datetime.datetime
    date_last_reply: datetime.datetime
    dept_id: int
    dept_name: str
    email: str
    flag: Optional[int]
    name: str
    notes: List[str]
    number: int
    priority: str
    replies: List[Dict[str, str]]
    service_id: Optional[str]
    status: str
    subject: str


class TicketBridge(base.BaseBridge):

    def create(self,
               subject: str,
               message: str,
               dept_id: int,
               client_id: Optional[int] = None,
               contact_id: Optional[int] = None,
               name: Optional[str] = None,
               email: Optional[str] = None,
               priority: Optional[str] = None,
               service_id: Optional[int] = None,
               domain_id: Optional[int] = None,
               admin: Optional[bool] = None,
               markdown: Optional[bool] = None,
               custom_fields: Optional[List[Any]] = None) -> int:
        """
        Open a ticket via WHMCS API method ``OpenTicket``.

        :param int dept_id: ID of department to open the ticket in
        :param str subject: Subject of the ticket
        :param str message: Message of the ticket
        :param int client_id: ID of client to create ticket for
        :param int contact_id:
            ID of the contact to create the ticket for (only if ``client_id`` is
            passed).
        :param str name: Name of the person opening the ticket
        :param str email: Email address of the person opening the ticket
        :param str priority:
            Priority to assign to the ticket (``low``, ``medium``, or ``high``)
        :param int service_id: Service to associate with ticket
        :param int domain_id: Domain to associate with ticket
        :param bool admin: Pass as ``True`` if admin user is opening ticket
        :param bool markdown:
            Pass as ``True`` if the ``message`` is markdown formatted.
        :param dict customfields: Customfields to associate with the ticket
        :return: ID of created ticket
        :rtype: int

        .. note::
            Parameters ``service_id`` and ``domain_id`` are mutually exclusive.

        .. note::
            If ``contact_id`` is passed, a corresponding ``client_id`` parameter
            must also be passed.
        """

        params = {
            k: v for k, v
            in {
                "subject": subject,
                "message": message,
                "deptid": dept_id,
                "clientid": client_id,
                "contactid": contact_id,
                "name": name,
                "email": email,
                "priority": string.capwords(priority) if priority else None,
                "serviceid": service_id,
                "domainid": domain_id,
                "admin": 1 if admin else 0,
                "markdown": 1 if markdown else 0,
                "customfields": custom_fields
            }.items()
            if v is not None
        }

        if all([service_id, domain_id]):
            raise TypeError(
                "Parameters service_id and domain_id are mutually exclusive"
            )

        if contact_id and not client_id:
            raise TypeError(
                "Parameter contact_id also requires client_id"
            )

        response = self.client.send_request("openticket", params=params)

        ticket = self.get(int(response['id']))

        return ticket

    def get(self, resource: int):
        """
        Get a ticket.

        :param int resource: ID of ticket to retrieve
        :return: Ticket
        :rtype: :class:`Ticket`
        """

        response = self.client.send_request(
            'getticket',
            params={'ticketid': resource}
        )

        if response['replies']:
            replies = [reply for reply in response['replies']['reply']]
        else:
            replies = []

        if response['notes']:
            notes = response['notes']
        else:
            notes = []

        ticket = Ticket(
            self,
            id=int(response['ticketid']),
            admin=response['admin'] or None,
            cc_email=response['cc'] or None,
            client_id=int(response['userid']),
            contact_id=int(response['contactid']) or None,
            date=datetime.datetime.strptime(response['date'], '%Y-%m-%d %H:%M:%S'),
            date_last_reply=datetime.datetime.strptime(response['date'], '%Y-%m-%d %H:%M:%S'),
            dept_id=int(response['deptid']),
            dept_name=response['deptname'],
            email=response['email'],
            flag=int(response['flag']) or None,
            name=response['name'],
            notes=notes,
            number=int(response['tid']),
            priority=response['priority'].lower(),
            replies=replies,
            service_id=response['service'] or None,
            status=response['status'].lower(),
            subject=response['subject']
        )

        return ticket

    def delete(self, resource: Union[int, Ticket]) -> None:
        """
        Delete a ticket.

        :param str resource: Ticket (or its ID) to delete
        :return: Does not return
        :rtype: None
        """

        self.client.send_request(
            'deleteticket',
            params={'ticketid': base.getid(resource)}
        )
