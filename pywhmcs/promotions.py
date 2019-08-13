from typing import List, Optional, Union
import dataclasses
import datetime

from pywhmcs import base
from pywhmcs import exceptions


@dataclasses.dataclass
class Promotion(base.BaseResource):
    id: int
    code: str
    applies_to: List[str]
    apply_once: bool
    cycles: Optional[str]
    date_expiration: datetime.datetime
    date_start: datetime.datetime
    existing_client: bool
    lifetime_promo: bool
    max_uses: int
    new_signups: bool
    notes: str
    once_per_client: bool
    recur_for: int
    recurring: bool
    requires: List[int]
    requires_existing: bool
    type: str
    upgrade_config: str
    upgrades: bool
    uses: int
    value: float


class PromotionsBridge(base.BaseBridge):

    def get(self, resource: str) -> Promotion:
        """
        Get promotion.

        :param int resource: Promotion code to retrieve
        :return: Promotion
        :rtype: :class:`Promotion`
        """

        response = self.client.send_request(
            'getpromotions',
            params={'code': resource}
        )

        whmcs_promotion = response['promotions']['promotion'][0]

        promotion = Promotion(
            self,
            id=int(whmcs_promotion['id']),
            code=whmcs_promotion['code'],
            applies_to=whmcs_promotion['appliesto'].split(','),
            apply_once=bool(whmcs_promotion['applyonce']),
            cycles=whmcs_promotion['cycles'],
            date_expiration=None,
            date_start=None,
            existing_client=bool(whmcs_promotion['existingclient']),
            lifetime_promo=bool(whmcs_promotion['lifetimepromo']),
            max_uses=int(whmcs_promotion['maxuses']),
            new_signups=bool(whmcs_promotion['newsignups']),
            notes=whmcs_promotion['notes'],
            once_per_client=bool(whmcs_promotion['onceperclient']),
            recur_for=int(whmcs_promotion['recurfor']),
            recurring=bool(whmcs_promotion['recurring']),
            requires=whmcs_promotion['requires'].split(','),
            requires_existing=bool(whmcs_promotion['requiresexisting']),
            type=whmcs_promotion['type'],
            upgrade_config=whmcs_promotion['upgradeconfig'],
            upgrades=bool(whmcs_promotion['upgrades']),
            uses=int(whmcs_promotion['uses']),
            value=float(whmcs_promotion['value']),
        )

        return promotion

    def list(self, detailed=True, marker=None, limit=None, **filters) -> List[Union[Promotion, str]]:
        """
        List promotions.

        :return: List ofromotion
        :rtype: List[:class:`Promotion`]
        """

        response = self.client.send_request('getpromotions', params=dict())

        matches = []
        for whmcs_promotion in response['promotions']['promotion']:
            promotion = Promotion(
                self,
                id=int(whmcs_promotion['id']),
                code=whmcs_promotion['code'],
                applies_to=whmcs_promotion['appliesto'].split(','),
                apply_once=bool(whmcs_promotion['applyonce']),
                cycles=whmcs_promotion['cycles'],
                date_expiration=None,
                date_start=None,
                existing_client=bool(whmcs_promotion['existingclient']),
                lifetime_promo=bool(whmcs_promotion['lifetimepromo']),
                max_uses=int(whmcs_promotion['maxuses']),
                new_signups=bool(whmcs_promotion['newsignups']),
                notes=whmcs_promotion['notes'],
                once_per_client=bool(whmcs_promotion['onceperclient']),
                recur_for=int(whmcs_promotion['recurfor']),
                recurring=bool(whmcs_promotion['recurring']),
                requires=whmcs_promotion['requires'].split(','),
                requires_existing=bool(whmcs_promotion['requiresexisting']),
                type=whmcs_promotion['type'],
                upgrade_config=whmcs_promotion['upgradeconfig'],
                upgrades=bool(whmcs_promotion['upgrades']),
                uses=int(whmcs_promotion['uses']),
                value=float(whmcs_promotion['value']),
            )
            matches.append(promotion)

        return matches
