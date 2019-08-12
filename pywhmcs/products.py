from typing import Any, Dict, List, Optional, Union
import dataclasses

from pywhmcs import base


@dataclasses.dataclass
class Product(base.BaseResource):
    id: int
    configoptions: List[Dict[str, Any]]
    customfields: List[str]
    description: Optional[str]
    group_id: int
    module: str
    name: str
    paytype: str
    pricing: Dict[str, Dict[str, str]]
    type: str


class ProductsBridge(base.BaseBridge):

    def get(self, resource: Union[str, int]) -> Product:
        """
        Get a product by ID

        :param product: ID of product to get
        :return: Product
        :rtype: :class:`Product`
        :raises: :class:`pywhmcs.exceptions.ProductNotFound`
        """

        response = self.client.send_request(
            'getproducts',
            params={'pid': int(resource)}
        )

        whmcs_product = response['products']['product'][0]

        product = Product(
            self,
            id=int(whmcs_product['pid']),
            configoptions=whmcs_product['configoptions']['configoption'],
            customfields=whmcs_product['customfields']['customfield'],
            description=whmcs_product['description'] or None,
            group_id=int(whmcs_product['gid']),
            module=whmcs_product['module'],
            name=whmcs_product['name'],
            paytype=whmcs_product['paytype'],
            pricing=whmcs_product['pricing'],
            type=whmcs_product['type']
        )

        return product

    def list(self, detailed=True, marker=None, limit=None, **kwargs) -> List[Product]:
        """
        List and filter products.

        :param str product_id: Product ID to filter by
        :param str group_id: Group ID to filter by
        :param str module: Module to filter by
        :return: Products matching given criteria
        :rtype: List[:class:`Product`]
        """

        params = {
            key: value for (key, value)
            in {
                'pid': kwargs.get('product_id'),
                'gid': kwargs.get('group_id'),
                'module': kwargs.get('module')
            }.items() if value is not None
        }

        response = self.client.send_request('getproducts', params)

        matches = []
        for whmcs_product in response['products']['product']:
            product = Product(
                self,
                id=int(whmcs_product['pid']),
                configoptions=whmcs_product['configoptions']['configoption'],
                customfields=whmcs_product['customfields']['customfield'],
                description=whmcs_product['description'] or None,
                group_id=int(whmcs_product['gid']),
                module=whmcs_product['module'],
                name=whmcs_product['name'],
                paytype=whmcs_product['paytype'],
                pricing=whmcs_product['pricing'],
                type=whmcs_product['type']
            )
            matches.append(product)

        return matches
