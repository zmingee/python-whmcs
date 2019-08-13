python-whmcs
============

This library is for interacting with the WHMCS external API, as described at
`WHMCS API Index <https://developers.whmcs.com/api/api-index/>`_. This library
exposes the API methods via a client interface, with separate modules for each
logical section of the API. Many of the API parameter names and values have
been changed to make the library easier to work with. The WHMCS API has some
strange corners, and this library attempts to smooth those out as much as
possible.

Installation
------------

Installation is simple:

::

    python setup.py install

Usage
-----

Usage is also simple:

::

    from pywhmcs import client
    import pprint
    c = client.Client(
        'https://whmcs.example.com/includes/api.php',
        username='admin',
        password='Sup3rS3cr3t'
    )
    client_account = c.clients.get('john.dough@example.com')
    invoices = c.invoices.list(client_id=client_account.id)
    for invoice in invoices:
        pprint.pprint(invoice.to_dict())

..  vim: set ts=8 sw=4 tw=79 et :
