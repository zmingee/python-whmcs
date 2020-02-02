__version_info__ = (1, 0, 0)
__version__ = '.'.join(map(str, __version_info__))

import logging

LOGGER: logging.Logger = logging.getLogger(__name__)
