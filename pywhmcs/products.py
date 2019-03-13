
from pywhmcs import base


class ProductsBridge(base.BaseBridge):

    def get_products(self, product_id: int = None, group_id: int = None,
                     module: str = None) -> dict:
        """
        Get products matching given criteria.

        :param int product_id: Limit search to specific product ID
        :param int group_id: Limit search to a specific product group ID
        :param str module: Limit search to products utilising a specific module
        :return: Products matching given criteria
        :rtype: dict
        """

        params = {
            "pid": product_id,
            "gid": group_id,
            "module": module
        }
        params = {k: v for k, v in params.items() if v is not None}

        response = self.client.send_request("GetProducts", params)

        if not response["numreturned"]:
            products = []
        else:
            products = response["products"]["product"]

        return {
            "total": int(response["totalresults"]),
            "products": products,
            "start_number": int(response["startnumber"])
        }


