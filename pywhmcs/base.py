from __future__ import annotations
from typing import Any, Dict, List, Union
import dataclasses
import logging

LOGGER = logging.getLogger(__name__)


def getid(obj):
    """
    Get object's ID or object.

    Allows for using a resource or its ID as a parameter.
    """

    try:
        return obj.id
    except AttributeError:
        return obj


@dataclasses.dataclass
class BaseResource:
    bridge: dataclasses.InitVar[BaseBridge]

    def __post_init__(self, bridge):
        self.bridge = bridge

    def delete(self) -> None:
        return self.bridge.delete(self) # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)

    def update(self, **kwargs) -> BaseResource:
        return self.bridge.update(self, **kwargs) # type: ignore


class BaseBridge:

    def __init__(self, client):
        self.client = client

    def list(self, detailed=True, marker=None, limit=None, **filters) -> List[Union[BaseResource, str]]:
        pass

    def update(self, resource, **properties):
        pass

    def delete(self, resource):
        pass
