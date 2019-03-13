import string

from pywhmcs import base


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

        return int(response["tid"])

    def get_tickets(self, start_number=0, limit=25, dept_id=None, client_id=None,
                    email=None, status=None, subject=None,
                    ignore_dept_assignments=False) -> dict:
        """
        Get a list of tickets.

        Gets a list of tickets matching the parameters passed.

        :param int start_number: Offset for the returned resources
        :param int limit: Number of resources to return
        :param int dept_id: Limit query to specific department ID
        :param int client_id: Limit query to specific client ID
        :param str email: Limit query to specific non-client email address
        :param str status: Limit query to those matching status
        :param str subject: Limit query to those matching subject
        :param bool ignore_dept_assignments:
            Pass as ``True`` to _not_ limit to the departments the calling user is
            a member of.
        :return: Tickets matching the defined parameters.
        :rtype: dict
        """

        params = {
            "limitstart": start_number,
            "limitnum": limit,
            "deptid": dept_id,
            "clientid": client_id,
            "email": email,
            "status": status,
            "subject": subject,
            "ignore_dept_assignments": ignore_dept_assignments
        }
        params = {k: v for k, v in params.items() if v is not None}

        response = self.client.send_request("GetTickets", params)

        if not response["numreturned"]:
            tickets = []
        else:
            tickets = response["tickets"]["ticket"]

        return {
            "total": int(response["totalresults"]),
            "tickets": tickets,
            "start_number": int(response["startnumber"])
        }

    def get_support_departments(self, ignore_dept_assignments=True):
        """
        Get WHMCS support departments.

        Also provides limited stats on the department.

        :return: List of WHMCS support departments
        :rtype: list
        """

        params = {"ignore_dept_assignments": ignore_dept_assignments}

        response = self.client.send_request("GetSupportDepartments", params)

        departments = []
        for department in response["departments"]["department"]:
            departments.append({
                "id": department["id"],
                "name": department["name"],
                "open_tickets": department["opentickets"],
                "awaiting_reply": department["awaitingreply"]
            })

        return departments

