from pywhmcs import base


class GeneralBridge(base.BaseBridge):

    def validate_login(self, email: str, password: str) -> None:
        """
        Validate a user's credential.

        :param str email: Email of client to authenticate
        :param str password: Password of client to authenticate
        :return: Does not return
        :rtype:
        """

        self.client.send_request(
            action='validatelogin',
            params={'email': email, 'password2': password}
        )
