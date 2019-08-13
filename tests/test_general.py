import pytest

from pywhmcs import exceptions


class TestGeneral:

    def test_validate_login(self, whmcs_client, client_account):
        whmcs_client.general.validate_login(client_account.email, 'Password123')

        with pytest.raises(exceptions.InvalidEmailOrPassword):
            whmcs_client.general.validate_login(client_account.email, 'invalid123')
