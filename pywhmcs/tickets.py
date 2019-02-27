import string

from pywhmcs import base
from pywhmcs import exceptions


class TicketBridge(base.BaseBridge):

    def open(self, subject, message, dept_id, client_id=None, contact_id=None,
             name=None, email=None, priority=None, service_id=None,
             domain_id=None, admin=False, markdown=False,
             customfields=None) -> int:
        """
        Open a ticket.

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
                "customfields": customfields
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

        response = self.client.send_request("OpenTicket", params)

        if response.get('result') == 'error':
            raise exceptions.UnknownError(response['message'])

        return int(response["tid"])
