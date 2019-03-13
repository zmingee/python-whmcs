
from pywhmcs import base
from pywhmcs import exceptions

class PromotionsBridge(base.BaseBridge):

    def get_promotion(self, promo_code: str) -> dict:
        """
        Get promotions
        :param promo_code: Promo code to get.
        """

        response = self.client.send_request("GetPromotions", params={"code": promo_code})

        if not response["totalresults"]:
            raise exceptions.ResourceNotFound

        if response["totalresults"] > 1:
            raise exceptions.ResourceNotUnique

        return response["promotions"]["promotion"][0]

    def list_promotions(self):
        """
        Get list of promotions.

        :return: List of promotions
        :rtype: list
        """

        response = self.client.send_request("GetPromotions")

        return response["promotions"]["promotion"]
